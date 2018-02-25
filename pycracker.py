#!/usr/bin/python3

import pycracker_def as func_lib

def main():
	func_lib.arg_Parser()
	var = func_lib.arg_Parser.options
	var1 = func_lib.arg_Parser.usg
	if var.user == None:
		func_lib.no_User(var, var1 )
	else:
		func_lib.w_User(var, var1 )


if __name__ == "__main__":
	main()