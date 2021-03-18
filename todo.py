# import argparse
# parser = argparse.ArgumentParser(description = 'Adds and subtracts')
# #parser.add_argument('echo', help='echoes back the arguments')
# #group = parser.add_mutually_exclusive_group()
# parser.add_argument('-a', '--add', nargs=2, help='adds two numbers', type=int)
# parser.add_argument('-s', '--sub', nargs=2, help='subtracts two numbers', type=int)
# #group.add_argument('-s', '--sub', help='subtracts two numbers', action='store_true')
# #parser.add_argument('x', type=int)
# #parser.add_argument('y', type=int)
# args = parser.parse_args()
# print(sum(args.add))

import uuid
import time
import argparse
import json


class Todo:
    def __init__(self, db: str) -> None:
        self.db = db
        with open(self.db, 'r') as f:
            self.tasks = json.load(f)

    def update_db(self):
        with open(self.db, 'w') as f:
            json.dump(self.tasks, f)

    def create_task(self, title: str, desc: str = None) -> int:
        """Create a task, takes title and optional description, returns uniqueid as int."""
        task = {
            'unix': int(time.time()),
            'title': title,
            'desc': desc,
            'status': False
        }
        self.tasks[(uid := uuid.uuid1().int)] = task
        self.update_db()
        return uid

    def list_tasks(self) -> None:
        print('*'*10)
        for i, j in self.tasks.items():
            print(f'{i}\t{j}')
        print('*'*10)

    def delete_task_by_id(self, id: int) -> dict:
        if (id := str(id)) in self.tasks:
            temp = self.tasks[id]
            del self.tasks[id]
            self.update_db()
            return temp
        else:
            return {}

    def delete_task_by_title(self, title: str, limit: int = 1) -> dict:
        """Delete a task by title, takes title string and optional limit, default 1. Returns a dictionary of all deleted task."""
        temp = []
        retemp = {}
        for i, j in self.tasks.items():
            if title in j['title']:
                temp.append(i)

        while limit > 0 and len(temp) > 0:
            for i in temp:
                retemp[i] = self.tasks[i]
                del self.tasks[i]
                temp.remove(i)
                break
            limit -= 1
        self.update_db()
        return retemp

    # def mark_as_complete(self, limit = 1, **args) -> str:
    #     "Marks task complete. If id given, uses that. If title given, completes all with same title for limit times, default 1"
    #     if 'id' in args:
    #         if args['id'] in self.tasks:
    #             self.tasks[args['id']]['status'] = True
    #             return f'{args["id"]} marked'
    #         else:
    #             return "Id not found"
    #     elif 'title' in args:
    #         for i, j in self.tasks.items():
    #             if limit < 1:
    #                 break
    #             elif args['title'] in j['title']:
    #                 self.tasks[i]['status'] = True
    #                 limit -= 1
    #             else:
    #                 return "Title not found"
    #     else:
    #         return "No valid parameters"

    def flip_complete_id(self, id: int) -> int:
        if id in self.tasks:
            if self.tasks[id]['status']:
                self.tasks[id]['status'] = False
                self.update_db()
                return id
            else:
                self.tasks[id]['status'] = True
                self.update_db()
                return id
        else:
            return 0

    def flip_complete_title(self, title, limit=1) -> tuple:
        temp = []
        for i, j in self.tasks.items():
            if limit < 1:
                break
            elif title in j['title']:
                if self.tasks[i]['status']:
                    self.tasks[i]['status'] = False
                    self.update_db()
                    temp.append(i)
                else:
                    self.tasks[i]['status'] = True
                    self.update_db()
                    temp.append(i)
                limit -= 1
            else:
                pass
        return tuple(temp)


if __name__ == '__main__':
    todo = Todo('db.json')
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', nargs='*', action='append', metavar=('title', 'desc'), help='Create a task', type=str)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--remove', action='store_true')
    group.add_argument('-f', '--flip', action='store_true')
    parser.add_argument('-i', '--id', type=int)
    parser.add_argument('-t', '--title', type=str)
    parser.add_argument('-l', '--limit', type=int)
    args = parser.parse_args()
    if args.create:
        for i in args.create:
            print(f'created {todo.create_task(i[0], " ".join(i[1:]))}')
    else:
        pass

    if args.remove:
        if args.id:
            print(f'removed {todo.delete_task_by_id(args.id)}')
        elif args.title:
            if args.limit:
                print(f'removed {todo.delete_task_by_title(args.title, args.limit)}')
            else:
                print(f'removed {todo.delete_task_by_title(args.title)}')

        else:
            print('Remove What!?')
    else:
        pass

    if args.flip:
        if args.id:
            print(f'flipped {todo.flip_complete_id}')
        elif args.title:
            if args.limit:
                print(f'flipped {todo.flip_complete_title(args.title, args.limit)}')
            else:
                print(f'flipped {todo.flip_complete_title(args.title)}')
        else:
            print('Flip what now!?')
    else:
        pass

    todo.list_tasks()
