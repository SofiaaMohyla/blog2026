from db import *
create_tables()
add_category("gamedev")
add_category("web")
add_category("personal")

add_post(1,
         "шось про геймдев",
         "2026-03-14 18:40")

add_post(2,
         "шось про веб",
         "2026-03-14 18:40")

show_posts(1)