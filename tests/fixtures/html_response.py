original_reponse = """<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Курсы по программированию Хекслет</title>
        <link rel="stylesheet" media="all" href="https://cdn2.hexlet.io/assets/menu.css">
        <link rel="stylesheet" media="all" href="/assets/application.css">
        <link href="/courses" rel="canonical">
    </head>
    <body>
        <img src="/assets/professions/nodejs.png" alt="Иконка профессии Node.js-программист">
        <h3>
            <a href="/professions/nodejs">Node.js-программист</a>
        </h3>
        <script src="https://js.stripe.com/v3/"></script>
        <script src="https://ru.hexlet.io/packs/js/runtime.js"></script>
    </body>
</html>"""  # noqa: E501

changed_html = """<!DOCTYPE html>
<html lang="ru">
 <head>
  <meta charset="utf-8"/>
  <title>
   Курсы по программированию Хекслет
  </title>
  <link href="https://cdn2.hexlet.io/assets/menu.css" media="all" rel="stylesheet"/>
  <link href="ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css" media="all" rel="stylesheet"/>
  <link href="ru-hexlet-io-courses_files/ru-hexlet-io-courses.html" rel="canonical"/>
 </head>
 <body>
  <img alt="Иконка профессии Node.js-программист" src="ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png"/>
  <h3>
   <a href="/professions/nodejs">
    Node.js-программист
   </a>
  </h3>
  <script src="https://js.stripe.com/v3/">
  </script>
  <script src="ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js">
  </script>
 </body>
</html>"""  # noqa: E501
