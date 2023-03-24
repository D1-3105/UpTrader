# Menu task
### Notes:
- Applied db already migrated
- To create page use admin panel. To apply menu to the page user constructor
- Constructor is available on admin site (change form -> "Click here to change on constructor!")
- Raw queries used in program on dir: BASE_DIR/menu/queries/
- I used extra BFS on python to protect from invalid root definition, because I had not enough time for testing >~<
- To create menu tree use admin site (not enough time for constructor :/)
- My contacts: 
__https://t.me/lucshe_tebia__, ~~lyerhd@gmail.com~~
# Opened issues
There is a bug (probably browser issue) - after constructor submit browser does not reload page. Even if it gets redirect it ignores reload of page.
# Menu creation
I've ran out of time, so I have not provided any of constructor for menu. Use Django admin to create it!
- Create menu element objects for menu
- Create menu object
- Create another menu and link it to the old menu's element. # You should not link same menus on the same tree more than one time

