CREATE DEFINER=`root`@`localhost` PROCEDURE `get_building_attributes`(IN col_name VARCHAR(255))
BEGIN
    SET @query = CONCAT('SELECT BLDG_VALUE, LAND_VALUE, GROSS_TAX, ', col_name, 
                        ' FROM boston_housing_21 WHERE ', col_name, 
                        ' IS NOT NULL AND ', col_name, ' <> ""');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END