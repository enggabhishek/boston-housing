CREATE DEFINER=`root`@`localhost` PROCEDURE `get_building_att_and_area`(IN col1 varchar(255), IN col2 varchar(255))
BEGIN
    SET @query = CONCAT('SELECT BLDG_VALUE, LAND_VALUE, GROSS_TAX, ', col1, ', ', col2, 
                        ' FROM boston_housing_21');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END