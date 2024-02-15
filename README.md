# Rinha de Backend - Django + PostgreSQL

Esta é a minha tentativa de implementar uma solução em django para a [Rinha de Backend](https://github.com/zanfranceschi/rinha-de-backend-2024-q1). Encaro isso mais como uma oportunidade de aprendizado dado que minha experiência com o desenvolvimento de APIs é limitada, assim como meus conhecimentos de Docker.

## Considerações

-   Esta não é uma submissão para ambiente de produção, uma vez que estou usando o built-in dev server do Django.
-   Não estou preocupado exatamente com a performance, mas sim em conseguir completar o projeto e submeter para participar da rinha.
-   Tenho praticamente zero experiência com dev-ops, então aprender docker, como integrar o banco de dados com o django, e entender as particularidades de se fazer o django rodar com o docker tem sido um grande desafio.

## O que aprendi até agora

### Aplicando migrações:

Rodar django em docker tem algumas complexidades, dado que é preciso aplicar database migrations e executar scripts antes da solução ficar disponível para acesso à API. Para rodar as migrações, estou utilizando multiplos shell commands na etapa do command do docker compose:

```docker
web:
    build: .
    command: >
      sh -c "python rinhadjango/manage.py migrate &&
             python rinhadjango/manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
    ports:
      - 8000:8000
    depends_on:
      - db
```

No entanto, existem alguns casos onde o banco de dados ainda não está disponível para o django realizar a migração. Desta forma, é preciso implementar no settings.py:

```python
# Checking if database is ready for migration
DATABASE_READY = False

# At startup
while not DATABASE_READY:
    try:
        django.db.connections['default'].ensure_connection()
    except Exception:
        time.sleep(1)
    else:
        DATABASE_READY = True

# Run migrations now
if not DATABASE_READY:
    print('Applying migrations...')
    os.system('python manage.py migrate')
```

Esta sugestão foi extraída do site [studygyaan.com](https://studygyaan.com/django/applying-django-database-migrations-with-docker-compose)

### Popular o banco de dados previamente

Para a Rinha, é preciso popular a base de clients no banco previamente. Para isso, ao invés de usar um script SQL, usei um script python que usa o ORM do django. No entanto, não é uma trabalho direto como criar um script e rodar, pois o django é uma aplicação isolada. Para isso, é preciso utilizar classes Command. Esse arquivo deve ser criado em app/management/commands/initdb.py:

```python
from ...models import Clientes
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, **options):

        limites = [100000, 80000, 1000000, 10000000, 500000]

        for lim in limites:
            cliente = Clientes(limite=lim, saldo_inicial=0)
            cliente.save()

        verificar = Clientes.objects.all()
        print(verificar)
```

E depois este comando ser chamado no shell:

```shell
python manage.py initdb
```

Mas como queremos implementar essa funcionalidade quando fizermos o docker-compose up, essa alteração no arquivo docker-compose.yml foi necessária:

```docker
  web:
    build: .
    command: >
      sh -c "python rinhadjango/manage.py migrate &&
             python rinhadjango/manage.py initdb &&
             python rinhadjango/manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
    ports:
      - 8000:8000
    depends_on:
      - db
```

Você pode encontrar mais informações sobre classes Command na [documentação](https://docs.djangoproject.com/en/dev/howto/custom-management-commands/) do Django.
