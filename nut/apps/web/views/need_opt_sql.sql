SELECT `core_selection_entity`.`id`,
       `core_selection_entity`.`entity_id`,
        `core_selection_entity`.`is_published`,
        `core_selection_entity`.`pub_time`,
        `core_entity`.`id`,
        `core_entity`.`user_id`,
        `core_entity`.`entity_hash`,
        `core_entity`.`category_id`,
        `core_entity`.`brand`,
        `core_entity`.`title`,
        `core_entity`.`intro`,
        `core_entity`.`rate`,
        `core_entity`.`price`,
        `core_entity`.`mark`,
        `core_entity`.`images`,
        `core_entity`.`created_time`, `core_entity`.`updated_time`, `core_entity`.`status` FROM `core_selection_entity` INNER JOIN `core_entity` ON ( `core_selection_entity`.`entity_id` = `core_entity`.`id` ) WHERE (`core_selection_entity`.`is_published` = True  AND `core_selection_entity`.`pub_time` <= 2016-03-20 09:23:53 ) ORDER BY `core_selection_entity`.`pub_time` DESC