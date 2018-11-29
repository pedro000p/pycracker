#!/usr/bin/python3

import pycracker_def as func_lib

def main():
	func_lib.arg_Parser()
	parser = func_lib.arg_Parser.options
	usage = func_lib.arg_Parser.usg
	if parser.user == None:
		func_lib.no_User(parser, usage )
	else:
		func_lib.w_User(parser, usage )


if __name__ == "__main__":
	main()
