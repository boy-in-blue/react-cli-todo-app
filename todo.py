import argparse
parser = argparse.ArgumentParser(description = "Adds and subtracts")
#parser.add_argument("echo", help="echoes back the arguments")
group = parser.add_mutually_exclusive_group()
group.add_argument("-a", "--add", help="adds two numbers", action="store_true")
group.add_argument("-s", "--sub", help="subtracts two numbers", action="store_true")
parser.add_argument("x", type=int)
parser.add_argument("y", type=int)
args = parser.parse_args()
if args.add:
    print(args.x + args.y)
elif args.sub:
    print(args.x - args.y)

