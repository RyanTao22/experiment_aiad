import streamlit as st
import pandas as pd
import ast
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# ------------------ Cached Resources ------------------

@st.cache_resource(show_spinner=False)
def get_engine():
    """返回单例 SQLAlchemy Engine，对所有查询共用同一连接池。

    说明：
    1. 通过 `@st.cache_resource` 装饰器保证在 **整个 Streamlit 会话** 中只执行一次
       `create_engine`，从而避免重复创建连接池。
    2. `pool_pre_ping=True` 会在将连接借出前自动做 *ping* 检测，若连接失效则自动重连，
       让长时间空闲后的连接依然可用。
    3. `pool_recycle=3600` 指定连接最大生命周期（秒），可防止 MySQL *wait_timeout* 导致的
       "MySQL server has gone away" 错误。
    """

    return create_engine(
        f"mysql+pymysql://{st.secrets['username']}:{st.secrets['password']}@"
        f"{st.secrets['db_url']}:{st.secrets['port']}/{st.secrets['database']}?charset=utf8mb4",
        pool_pre_ping=True,
        pool_recycle=3600,
    )

# ------------------ Cached Data ------------------

@st.cache_data(show_spinner=False)
def fetch_ad_ts(team: str, product: str):
    """Query ad metadata rows matching team & product."""
    engine = get_engine()
    sql = text(
        """
        SELECT sid,
               team,
               product,
               prompt,
               script   AS refine_script,
               age_range AS Age_Range,
               gender    AS Gender,
               household_income AS Household_Income,
               ethnicity AS Ethnicity
        FROM ad_ts
        WHERE team = :team AND product = :product
        """
    )
    df = pd.read_sql(sql, engine, params={"team": team, "product": product})
    df['sid'] = df['sid'].astype(int)
    return df

@st.cache_data(show_spinner=False)
def fetch_video_detail(sid: int):
    """Return one-row DataFrame with video info for a given sid."""
    engine = get_engine()
    sql = text(
        """
        SELECT narrator_start_timestamps,
               narrator_durations,
               bgm_url
        FROM video_df
        WHERE sid = :sid
        """
    )
    df = pd.read_sql(sql, engine, params={"sid": int(sid)})
    df['narrator_start_timestamps'] = df['narrator_start_timestamps'].apply(ast.literal_eval)
    df['narrator_durations'] = df['narrator_durations'].apply(ast.literal_eval)
    return df.iloc[0]

def _build_ad_query(filters: dict):
    """Construct SQL and params based on optional demographic filters."""
    column_map = {
        'Age_Range': 'age_range',
        'Gender': 'gender',
        'Household_Income': 'household_income',
        'Ethnicity': 'ethnicity',
    }

    sql_parts = [
        "SELECT sid, prompt, script AS refine_script FROM ad_ts",
        "WHERE team = :team AND product = :product"
    ]
    params = {}
    for key, val in filters.items():
        if val is not None and key in column_map:
            col = column_map[key]
            sql_parts.append(f"AND {col} = :{col}")
            params[col] = val
    final_sql = " " .join(sql_parts)
    return text(final_sql), params


def fetch_candidate_ads(team: str, product: str, filters: dict):
    """Return DataFrame (sid, prompt, refine_script) that meets given filters."""
    engine = get_engine()
    sql, dynamic_params = _build_ad_query(filters)
    params = {"team": team, "product": product, **dynamic_params}
    df = pd.read_sql(sql, con=engine, params=params)
    df['sid'] = df['sid'].astype(int)
    return df 