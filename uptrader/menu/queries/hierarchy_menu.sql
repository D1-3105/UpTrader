WITH pivot as (
	SELECT DISTINCT menuelement_id, menu_id as menu_id FROM menu_menu_elements
	LEFT JOIN menu_menu
	ON menu_menu.id = menu_menu_elements.menu_id
	WHERE menu_menu.menu_name = %s -- Add id here
	ORDER BY 'order'
),
menu_tree(menu_id, id, header, 'order', menu_child_id) AS (
	SELECT DISTINCT t2.menu_id,
					root.id,
					root.header,
					root.'order',
					root.menu_child_id
	FROM menu_menuelement root, pivot as t2
	WHERE id in (
					SELECT menuelement_id FROM pivot
				)
	UNION ALL
	SELECT  old.menu_child_id, new.id, new.header, new.'order', new.menu_child_id as new_root
	FROM menu_tree old
	JOIN menu_menuelement new ON new.id in (
					SELECT menuelement_id FROM menu_menu_elements
					LEFT JOIN menu_menu
					ON menu_menu.id = menu_menu_elements.menu_id
					WHERE menu_menu.id = old.menu_child_id
					ORDER BY 'order'
				)
),
-- now slice the tree to not overhead in python
sliced_tree(menu_id, menu_child_id) as (
	SELECT  menu_id, menu_child_id FROM menu_tree root
	WHERE root.menu_id = %s
	UNION ALL
	SELECT new_els.menu_id, root.menu_id FROM sliced_tree root
	LEFT JOIN menu_tree new_els ON new_els.menu_child_id = root.menu_id
	WHERE new_els.menu_child_id is not NULL
)
SELECT * FROM menu_tree elements
WHERE elements.menu_id IN (SELECT menu_id FROM sliced_tree)
ORDER BY elements.menu_id, elements.'order';
