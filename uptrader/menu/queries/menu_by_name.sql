-- Select distinctly menu-related ids of menu with such name
WITH menu_tmp as (
                    SELECT DISTINCT menuelement_id FROM menu_menu_elements
                    LEFT JOIN  menu_menu
                    ON menu_menu.id = menu_menu_elements.menu_id
                    WHERE menu_menu.menu_name = %s
                )
-- Select all elements with returned ids
SELECT *
FROM menu_menuelement
WHERE id IN menu_tmp
ORDER BY 'order';
