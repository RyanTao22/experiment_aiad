DROP TABLE IF EXISTS group_counts;

CREATE TABLE group_counts ( 
    test_group_name VARCHAR(50),
    product VARCHAR(50),
    excel_team  VARCHAR(50),
    filter_fields TEXT,
    current_count INT DEFAULT 0,
    max_count INT,
    is_done BOOLEAN DEFAULT FALSE,
    last_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (test_group_name)
);


# Ice Cream Tub(Breyers)   'Wine(Harlan Estate)' 'Laptop(MacBook)'  'Toothpaste(Colgate)'   
INSERT INTO group_counts (test_group_name, product, excel_team, filter_fields, current_count, max_count, is_done, last_update_timestamp) VALUES 
('A1_icecream_all_demo', 'Ice Cream Tub(Breyers)', 'Condition_3', '["Age_Range", "Gender", "Household_Income", "Ethnicity"]', 0, 108, FALSE, NOW()),

('A21_icecream_partly_demo_age', 'Ice Cream Tub(Breyers)', 'Condition_3_one_var', '["Age_Range"]', 0, 27, FALSE, NOW()),
('A22_icecream_partly_demo_gender', 'Ice Cream Tub(Breyers)', 'Condition_3_one_var', '["Gender"]', 0, 27, FALSE, NOW()),
('A23_icecream_partly_demo_income', 'Ice Cream Tub(Breyers)', 'Condition_3_one_var', '["Household_Income"]', 0, 27, FALSE, NOW()),
('A24_icecream_partly_demo_ethnicity', 'Ice Cream Tub(Breyers)', 'Condition_3_one_var', '["Ethnicity"]', 0, 27, FALSE, NOW()),

('A3_icecream_no_demo', 'Ice Cream Tub(Breyers)', 'Condition_2', '[]', 0, 108, FALSE, NOW()),

('A4_icecream_human_ad', 'Ice Cream Tub(Breyers)', 'Condition_1', '[]', 0, 108, FALSE, NOW()),


# Wine(Harlan Estate)
('B1_wine_all_demo', 'Wine(Harlan Estate)', 'Condition_3', '["Age_Range", "Gender", "Household_Income", "Ethnicity"]', 0, 108, FALSE, NOW()),   

('B21_wine_partly_demo_age', 'Wine(Harlan Estate)', 'Condition_3_one_var', '["Age_Range"]', 0, 27, FALSE, NOW()),
('B22_wine_partly_demo_gender', 'Wine(Harlan Estate)', 'Condition_3_one_var', '["Gender"]', 0, 27, FALSE, NOW()),
('B23_wine_partly_demo_income', 'Wine(Harlan Estate)', 'Condition_3_one_var', '["Household_Income"]', 0, 27, FALSE, NOW()),
('B24_wine_partly_demo_ethnicity', 'Wine(Harlan Estate)', 'Condition_3_one_var', '["Ethnicity"]', 0, 27, FALSE, NOW()),

('B3_wine_no_demo', 'Wine(Harlan Estate)', 'Condition_2', '[]', 0, 108, FALSE, NOW()),

('B4_wine_human_ad', 'Wine(Harlan Estate)', 'Condition_1', '[]', 0, 108, FALSE, NOW()),

# Laptop(MacBook)
('C1_laptop_all_demo', 'Laptop(MacBook)', 'Condition_3', '["Age_Range", "Gender", "Household_Income", "Ethnicity"]', 0, 108, FALSE, NOW()),

('C21_laptop_partly_demo_age', 'Laptop(MacBook)', 'Condition_3_one_var', '["Age_Range"]', 0, 27, FALSE, NOW()),
('C22_laptop_partly_demo_gender', 'Laptop(MacBook)', 'Condition_3_one_var', '["Gender"]', 0, 27, FALSE, NOW()),
('C23_laptop_partly_demo_income', 'Laptop(MacBook)', 'Condition_3_one_var', '["Household_Income"]', 0, 27, FALSE, NOW()),
('C24_laptop_partly_demo_ethnicity', 'Laptop(MacBook)', 'Condition_3_one_var', '["Ethnicity"]', 0, 27, FALSE, NOW()),

('C3_laptop_no_demo', 'Laptop(MacBook)', 'Condition_2', '[]', 0, 108, FALSE, NOW()),

('C4_laptop_human_ad', 'Laptop(MacBook)', 'Condition_1', '[]', 0, 108, FALSE, NOW()),

# Toothpaste(Colgate)
('D1_toothpaste_all_demo', 'Toothpaste(Colgate)', 'Condition_3', '["Age_Range", "Gender", "Household_Income", "Ethnicity"]', 0, 108, FALSE, NOW()),

('D21_toothpaste_partly_demo_age', 'Toothpaste(Colgate)', 'Condition_3_one_var', '["Age_Range"]', 0, 27, FALSE, NOW()),
('D22_toothpaste_partly_demo_gender', 'Toothpaste(Colgate)', 'Condition_3_one_var', '["Gender"]', 0, 27, FALSE, NOW()),
('D23_toothpaste_partly_demo_income', 'Toothpaste(Colgate)', 'Condition_3_one_var', '["Household_Income"]', 0, 27, FALSE, NOW()),
('D24_toothpaste_partly_demo_ethnicity', 'Toothpaste(Colgate)', 'Condition_3_one_var', '["Ethnicity"]', 0, 27, FALSE, NOW()),

('D3_toothpaste_no_demo', 'Toothpaste(Colgate)', 'Condition_2', '[]', 0, 108, FALSE, NOW()),

('D4_toothpaste_human_ad', 'Toothpaste(Colgate)', 'Condition_1', '[]', 0, 108, FALSE, NOW());