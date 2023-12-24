<h5 align="center"><img src="https://github.com/A-V-tor/simple-solution/blob/main/img-1.png"></h5>
<h5 align="center"><img src="https://github.com/A-V-tor/simple-solution/blob/main/img-2.png"></h5>
<hr>
<h1 align="center">Развертывание проекта</h1>
Скачать проект

```
  git clone git@github.com:A-V-tor/simple-solution.git
```

```
  cd simple-solution
```

В корне проекта создать файл `.env`

```
    SECRET_KEY=ключ для шифрования сессий
    SECRET_API_STRIPE= секретный ключ с https://dashboard.stripe.com/test/apikeys
    PUBLISH_API_STRIPE= публичный ключ с https://dashboard.stripe.com/test/apikeys
    HOST=имя хоста для запуска

```

Запустить сборку докер-compose
```
docker-compose up -d
```