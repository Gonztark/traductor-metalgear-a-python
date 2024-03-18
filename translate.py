def translate_to_python(ast):
    python_code = ""
    for node in ast:
        python_code += translate_statement(node) + "\n"
    return python_code.strip()

def translate_expression(expr):
    if expr['type'] == 'binary_operation':
        left = translate_expression(expr['left'])
        right = translate_expression(expr['right'])
        return f"{left} {expr['operator']} {right}"
    elif expr['type'] == 'unary_operation':
        operand = translate_expression(expr['operand'])
        return f"{expr['operator']}{operand}"
    elif expr['type'] == 'number':
        if isinstance(expr['value'], int):
            return str(expr['value'])
        elif isinstance(expr['value'], float):
            return str(expr['value']).rstrip('0').rstrip('.')
    elif expr['type'] == 'variable':
        return expr['name']
    elif expr['type'] == 'comparison':
        left = translate_expression(expr['left'])
        right = translate_expression(expr['right'])
        return f"{left} {expr['operator']} {right}"
    elif expr['type'] == 'string':
        return f'"{expr["value"]}"'

def translate_function_declaration(node):
    name = node['name']
    params = ', '.join([param[1] for param in node['params']])
    body = translate_block(node['body'])

    # Find variables used in the function body that are declared outside the function
    global_vars = set()
    for statement in node['body']:
        global_vars.update(find_global_vars(statement))

    # Add global variable declarations at the beginning of the function body
    if global_vars:
        global_vars_declaration = "    global " + ", ".join(global_vars) + "\n"
        body = global_vars_declaration + body

    return f"def {name}({params}):\n{body}"

def find_global_vars(node):
    global_vars = set()
    if node['type'] == 'var_assignment':
        global_vars.add(node['name'])
    elif node['type'] == 'if':
        for statement in node['body']:
            global_vars.update(find_global_vars(statement))
    elif node['type'] == 'while':
        for statement in node['body']:
            global_vars.update(find_global_vars(statement))
    return global_vars

def translate_if_statement(node):
    condition = translate_expression(node['condition'])
    body = translate_block(node['body'])
    return f"if {condition}:\n    {body}"

def translate_if_else_statement(node):
    condition = translate_expression(node['condition'])
    if_body = translate_block(node['if_body'])
    else_body = translate_block(node['else_body'])
    return f"if {condition}:\n{if_body}\nelse:\n{else_body}"

def translate_while_statement(node):
    condition = translate_expression(node['condition'])
    body = translate_block(node['body'])
    return f"while {condition}:\n{body}"

def translate_block(block):
    python_code = ""
    for statement in block:
        python_code += "    " + translate_statement(statement) + "\n"
    return python_code

def translate_statement(statement):
    if statement['type'] == 'var_declaration':
        if statement['value']['type'] == 'function_call':
            value = translate_function_call(statement['value'])
        else:
            value = translate_expression(statement['value'])
        return f"{statement['name']} = {value}"

    elif statement['type'] == 'var_assignment':
        # cuando es una llamada de función asignando a una variable
        if statement['value']['type'] == 'function_call':
            value = translate_function_call(statement['value'])
        else:
            value = translate_expression(statement['value'])
        return f"{statement['name']} = {value}"

    elif statement['type'] == 'function_declaration':
        return translate_function_declaration(statement)

    elif statement['type'] == 'if':
        return translate_if_statement(statement)

    elif statement['type'] == 'if_else':
        return translate_if_else_statement(statement)

    elif statement['type'] == 'while':
        return translate_while_statement(statement)

    elif statement['type'] == 'for':
        variable = statement['init']['name']
        start = translate_expression(statement['init']['value'])
        end = translate_expression(statement['condition']['right'])
        body = translate_block(statement['body'])
        return f"for {variable} in range({start}, {end}):\n{body}"

    elif statement['type'] == 'print':
        return f"print({translate_expression(statement['value'])})"

    elif statement['type'] == 'function_call':
        # funciones directas como statements
        return translate_function_call(statement)

    elif statement['type'] == 'return':
        return f"return {translate_expression(statement['value'])}"


def translate_function_call(node):
    name = node['name']
    arguments = ', '.join([translate_expression(arg) for arg in node['arguments']])
    return f"{name}({arguments})"