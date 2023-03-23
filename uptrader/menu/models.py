from django.db import models, connection
from django.utils.functional import cached_property
from django.conf import settings


class MenuQuerySet(models.QuerySet):
    model: 'Menu'

    @staticmethod
    def flatten_clauses(table_name, **clauses):
        assert clauses
        on_ret = []
        for field_name in clauses.keys():
            on_ret.append(f'{table_name}.{field_name} = %s')
        return ' '.join(on_ret)


class MenuManager(models.Manager):

    def get_queryset(self):
        return MenuQuerySet(model=self.model, using=self._db)

    @cached_property
    def by_name_query(self):
        with open(settings.BASE_DIR/'menu/queries/menu_by_name.sql', 'r') as f:
            return f.read()

    def elements_by_menu_name(self, menu_name):
        """
            Call sql cached property
        """
        return self.get_queryset().raw(
            raw_query=self.by_name_query,
            params=[menu_name]
        )


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
        with open(settings.BASE_DIR/'menu/queries/hierarchy_menu.sql', 'r') as sql_holder:
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
