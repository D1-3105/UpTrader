from django.db import models, connection
from django.utils.functional import cached_property


class MenuQuerySet(models.QuerySet):
    model: 'Menu'

    @staticmethod
    def flatten_clauses(table_name, **clauses):
        assert clauses
        on_ret = []
        for field_name in clauses.keys():
            on_ret.append(f'{table_name}.{field_name} = %s')
        return ' '.join(on_ret)

    def elements_by_menu(self, **clauses):
        """
            Returns raw queryset with element info
        """
        e_table_name = MenuElement.table_name()
        through_table_name = self.model.elements.through._meta.db_table
        m_table_name = self.model.table_name()
        WHERE_CLAUSE = 'WHERE ' + self.flatten_clauses(m_table_name, **clauses)
        return self.raw(
            raw_query=
            f"""
                -- Select distinctly menu-related ids of menu with such name
                WITH menu_tmp as (
                    SELECT DISTINCT menuelement_id FROM {through_table_name} 
                    LEFT JOIN  {m_table_name}
                    ON menu_menu.id = {through_table_name}.menu_id
                    {WHERE_CLAUSE}
                )
                -- Select all elements with returned ids
                SELECT * 
                FROM {e_table_name}
                WHERE id IN menu_tmp
                ORDER BY 'order';
            """,
            params=(clauses.values())
        )


class MenuManager(models.Manager):
    def get_queryset(self):
        return MenuQuerySet(model=self.model, using=self._db)

    def elements_by_menu_name(self, menu_name):
        """
        Proxy to qs
        """
        return self.get_queryset().elements_by_menu(menu_name=menu_name)


class Menu(models.Model):
    """
    menu_parent->|->menu_child
                 |->menu_child
                 |->menu_child
                 |->menu_child
    """
    elements = models.ManyToManyField(
        to='MenuElement', blank=True
    )
    menu_name = models.CharField(
        max_length=100, unique=True
    )
    objects = MenuManager()

    def __str__(self):
        return self.menu_name

    @classmethod
    def table_name(cls) -> str:
        return cls._meta.db_table


class ElementQuerySet(models.QuerySet):
    model: 'MenuElement'


class ElementManager(models.Manager):
    def get_queryset(self):
        return ElementQuerySet(model=self.model, using=self._db)

    def raw(self, *args, **kwargs):
        return self.get_queryset().raw(*args, **kwargs)

    @cached_property
    def tree_query(self):
        with open('menu/queries/hierarchy_menu.sql', 'r') as sql_holder:
            tree_query = str(sql_holder.read())
            assert tree_query
            return tree_query

    def get_element_tree(self, root_name: str, till_id: int):
        """
            root_name - root element name
            till_id - element of tree that ends
        """
        with connection.cursor() as cursor:
            sql = str(self.tree_query)
            cursor.execute(sql, params=[str(root_name), till_id])
            cols = [col[0] for col in cursor.description]
            return [
                dict(zip(cols, row))
                for row in cursor.fetchall()
            ]


class MenuElement(models.Model):
    """
        Menu element
    """
    header = models.CharField(max_length=50)
    order = models.SmallIntegerField(default=0)
    menu_child = models.ForeignKey(to='Menu', related_name='child', null=True, blank=True, on_delete=models.SET_NULL)
    objects = ElementManager()

    def __str__(self):
        return '; '.join(
            (
                self.header,
                str(self.order)
            )
        )

    @classmethod
    def table_name(cls) -> str:
        return cls._meta.db_table

# Create your models here.
