def operatorValidity(string):

    operatorList=["SELECT",
                  "PROJECT",
                  "JOIN",
                  "RENAME",
                  "UNION",
                  "DIFFERENCE"]
    for op in operatorList:
        if op in string:
            return True
    return False



