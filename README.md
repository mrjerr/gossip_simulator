# Симулятор протокола эпидемий

## Пример запуска согласно заданию

**Сценарий необходимо выполнять для версии интерпретатора python не ниже 3.6**
```
> ./simulate.py -n 20 -i 1000
In 79.9% cases all nodes received the packet
Average iterations for complited cases: 81.0
Average iterations for uncomplited cases: 76.46268656716418

> ./simulate.py -n 20 -i 1000 --ignore-sender
In 84.2% cases all nodes received the packet
Average iterations for complited cases: 81.0
Average iterations for uncomplited cases: 76.64556962025317
```
**в случае отсутсвия нужной версии python интерпритатора, можно запустить с помощью
Docker контейнера python 3.6**
```
docker run -it --rm -v "$PWD":/code -w /code python:alpine3.6 python simulate.py -n 20 -i 1000
```


### Комментарии по выполнению задания.

Для того что бы корректно выполнить условие задания, необходимо для разных вариантов алгоритма
создать одинаково воспроизводимые условия случайного выбора.
По этому используется **random.seed**.

В сценарии доступен вариант указания произвольного seed:

```
> ./simulate.py -n 20 -i 1000 -s qwerty
In 81.4% cases all nodes received the packet

> /simulate.py -n 20 -i 1000 -s qwerty --ignore-sender
In 86.3% cases all nodes received the packet
```

Рассуждая о вариантах повышения эффективности алгоритма, пришел к выводу что нет возможности использовать какие-то структуры данных со связями между узлами. Поскольку с точки зрения реального узла сети, он вправе делать любой случайный выбор, доступных ему узлов. Следовательно повлиять на случайный выбор невозможно. Единственным возможным вариантов оптимизации - не отвечать узлу от которого пришел запрос. Собственно этот вариант я реализовал.
