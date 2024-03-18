import ply.yacc as yacc
from lexico import tokens, reset_lines

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LT', 'LTE', 'GT', 'GTE', 'NE'),
    ('right', 'UMINUS'),
)

# diccionario para almacenar las variables
symbol_table = {}
symbol_table_aux = {}
function_table = {}

results = ""

def p_program(p):
    '''program : program statement
               | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_expr(p):
    'statement : expression SEMICOLON'
    p[0] = {'type': 'expression', 'value': p[1]}

def p_statement_assign(p):
    '''statement : VAR ID ASSIGN expression SEMICOLON
                 | ID ASSIGN expression SEMICOLON'''
    if len(p) == 6:
        if p[2] not in symbol_table_aux:
            symbol_table_aux[p[2]] = {'value': p[4], 'type': type(p[4]).__name__}
            if p[2] not in symbol_table:
                symbol_table[p[2]] = {'value': p[4], 'type': type(p[4]).__name__}
            p[0] = {'type': 'var_declaration', 'name': p[2], 'value': p[4]}
        else:
            append_result(f"Error semántico (línea {p.lineno(2)}): La variable '{p[2]}' ya ha sido declarada.")
    else:
        if p[1] not in symbol_table:
            append_result(f"Error semántico (línea {p.lineno(1)}): La variable '{p[1]}' no ha sido declarada")
        else:
            p[0] = {'type': 'var_assignment', 'name': p[1], 'value': p[3]}

def p_statement_function(p):
    '''statement : FUNCTION ID LPARENT RPARENT block
                 | FUNCTION ID LPARENT param_list RPARENT block'''
    function_name = p[2]
    if function_name in function_table:
        append_result(f"Error semántico (línea {p.lineno(2)}): La función '{function_name}' ya ha sido declarada.")
    else:
        if len(p) == 6:
            function_table[function_name] = {'parameters': [], 'block': p[5]}
            p[0] = {'type': 'function_declaration', 'name': function_name, 'params': [], 'body': p[5]}
        else:
            function_table[function_name] = {'parameters': p[4], 'block': p[6]}
            for param in p[4]:
                symbol_table[param[1]] = None  
            p[0] = {'type': 'function_declaration', 'name': function_name, 'params': p[4], 'body': p[6]}

def p_param_list(p):
    '''param_list : param_list COMMA VAR ID
                  | VAR ID'''
    if len(p) == 5:
        p[0] = p[1] + [(p[3], p[4])]
    else:
        p[0] = [(p[1], p[2])]

def p_statement_if(p):
    '''statement : IF LPARENT expression RPARENT block
                 | IF LPARENT expression RPARENT block ELSE block'''
    if len(p) == 6:
        p[0] = {'type': 'if', 'condition': p[3], 'body': p[5]}
    else:
        p[0] = {'type': 'if_else', 'condition': p[3], 'if_body': p[5], 'else_body': p[7]}

def p_statement_while(p):
    'statement : WHILE LPARENT expression RPARENT block'
    p[0] = {'type': 'while', 'condition': p[3], 'body': p[5]}

def p_statement_for(p):
    'statement : FOR LPARENT statement expression SEMICOLON statement RPARENT block'
    p[0] = {'type': 'for', 'init': p[3], 'condition': p[4], 'step': p[6], 'body': p[8]}

def p_statement_return(p):
    'statement : RETURN expression SEMICOLON'
    p[0] = {'type': 'return', 'value': p[2]}

def p_block(p):
    '''block : LBRACE statements RBRACE
             | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    
    if 'value' not in p[1]:
        print("value")
    else:
        print("MEEEEEEERUNTEEEEEEEEEEEEE")
        print(p[1])
        print(p[3])
        try:
            left_type = p[1]['value']['type']
        except (TypeError, ValueError) as e:
            left_type = p[1]['type']
        except:
            return

        try:
            right_type = p[3]['value']['type']
        except (TypeError, ValueError) as e:
            right_type = p[3]['type']
        except:
            return

        
        if left_type == 'dict':
            left_type = p[1]['value']['value']['type']
        if right_type == 'dict':
            right_type = p[3]['value']['value']['type']
        if left_type == 'float':
            left_type = 'number'
        if right_type == 'float':
            right_type = 'number'
        
        print(p[1])
        print(left_type)
        print(right_type)

        if left_type != right_type:
            append_result(f"Error de tipos (línea {p.lineno(2)}): No se pueden realizar operaciones entre tipos diferentes ({left_type} y {right_type}).")
        else:
            p[0] = {'type': 'binary_operation', 'operator': p[2], 'left': p[1], 'right': p[3]}

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = {'type': 'unary_operation', 'operator': '-', 'operand': p[2]}

def p_expression_function_call(p):
    'expression : CALL ID LPARENT arguments RPARENT'
    function_name = p[2]
    if function_name in function_table:
        expected_params = function_table[function_name]['parameters']
        provided_args = p[4]

        if len(provided_args) != len(expected_params):
            append_result(f"Error semántico (línea {p.lineno(2)}): Número incorrecto de argumentos para la función '{function_name}'. Esperado: {len(expected_params)}, proporcionado: {len(provided_args)}.")
        else:
            auxfor = 0;
            for param in expected_params:
                if param[1] in symbol_table:
                    print(symbol_table)
                    symbol_table[param[1]] = {'value': {'type': type(provided_args[auxfor]['value']).__name__, 'value': provided_args[auxfor]['value']}, 'type': 'variable'}
                    auxfor = auxfor+1
                    print(symbol_table)
                    print(provided_args[1]['value'])
                    print("WAAASSAAAAAAAAA")
        p[0] = {'type': 'function_call', 'value': 'some_return_value', 'name': function_name, 'arguments': provided_args}
    else:
        print(function_table)
        append_result(f"Error semántico(línea {p.lineno(2)}): La función '{function_name}' no ha sido declarada.")
        p[0] = {'type': 'undefined_function_call', 'name': function_name, 'arguments': p[4]}


def p_expression_group(p):
    'expression : LPARENT expression RPARENT'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = {'type': 'number', 'value': p[1]}

def p_expression_name(p):
    'expression : ID'
    try:
        variable = symbol_table[p[1]]
        if variable is None:
            p[0] = {'type': 'variable', 'name': p[1], 'value': None}
        else:
            p[0] = {'type': 'variable', 'name': p[1], 'value': variable['value']}
        p.set_lineno(0, p.lineno(1))
    except LookupError:
        nr = f"Error semántico (línea {p.lineno(1)}): La variable '{p[1]}' no existe."
        append_result(nr)
        p[0] = {'type': 'undefined', 'name': p[1]}

def p_expression_comparison(p):
    '''expression : expression LT expression
                  | expression LTE expression
                  | expression GT expression
                  | expression GTE expression
                  | expression NE expression
                  | expression EQ expression'''
    print("EOOOO")
    print(p[1])
    print(p[3])
    left_type = p[1]['type']
    right_type = p[3]['type']

    if right_type == 'variable':
        right_type = p[3]['value']['type']
    if left_type == 'variable':
        left_type = p[1]['value']['type']
    if left_type == 'float':
        left_type = 'number'
    if right_type == 'float':
        right_type = 'number'

    if left_type != right_type:
        append_result(f"Error de tipos (línea {p.lineno(2)}): No se pueden comparar valores de diferentes tipos ({left_type} y {right_type}).")
    else:
        p[0] = {'type': 'comparison', 'operator': p[2], 'left': p[1], 'right': p[3]}

def p_expression_string(p):
    'expression : STRING'
    p[0] = {'type': 'string', 'value': p[1]}

def p_statement_print(p):
    'statement : PRINT LPARENT expression RPARENT SEMICOLON'
    p[0] = {'type': 'print', 'value': p[3]}

def p_statement_summon(p):
    'statement : CALL ID LPARENT arguments RPARENT SEMICOLON'
    function_name = p[2]
    if function_name in function_table:
        expected_params = function_table[function_name]['parameters']
        provided_args = p[4]
        if len(provided_args) != len(expected_params):
            append_result(f"Error semántico (línea {p.lineno(2)}): Número incorrecto de argumentos para la función '{function_name}'. Esperado: {len(expected_params)}, proporcionado: {len(provided_args)}.")
            print(f"Error semántico (línea {p.lineno(2)}): Número incorrecto de argumentos para la función '{function_name}'. Esperado: {len(expected_params)}, proporcionado: {len(provided_args)}.")
        else:
            auxfor = 0;
            for param in expected_params:
                if param[1] in symbol_table:
                    print(symbol_table)
                    symbol_table[param[1]] = {'value': {'type': type(provided_args[auxfor]['value']).__name__, 'value': provided_args[auxfor]['value']}, 'type': 'variable'}
                    auxfor = auxfor+1
                    print(symbol_table)
                    print("WAAASSAAAAAAAAA")
        p[0] = {'type': 'function_call', 'name': function_name, 'arguments': provided_args}
    else:
        append_result(f"Error semántico (línea {p.lineno(2)}): La función '{function_name}' no ha sido declarada.")
        print(f"Error semántico (línea {p.lineno(2)}): La función '{function_name}' no ha sido declarada.")
        p[0] = {'type': 'undefined_function_call', 'name': function_name, 'arguments': p[4]}
def p_arguments(p):
    '''arguments : arguments COMMA expression
                 | expression
                 | empty'''
    if len(p) == 2:
        if p[1] is None:  # Si es una lista vacía
            p[0] = []
        else:  # Si es una expresión única
            p[0] = [p[1]]
    elif len(p) > 2:
        p[1].append(p[3])
        p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None

def append_result(message):
    global results
    results += message + "\n"

def p_error(p):
    if p:
        append_result(f"Error de Sintaxis en '{p.value}' en la línea {p.lineno}")
        print(f"Error de Sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        aux = "Error de Sintaxis al final del código"
        append_result(aux)
        print(aux)

parser = yacc.yacc(debug=False)

def first_analysis(data):
    global symbol_table, function_table, results
    symbol_table.clear()
    function_table.clear()
    results = ""
    parser.parse(data, debug=False)

def second_analysis(data):
    global symbol_table, results, function_table, symbol_table_aux
    symbol_table_aux.clear()
    function_table.clear()
    results = ""
    ast = parser.parse(data, debug=False)
    return ast

def analizar_sintactico(data):
    first_analysis(data)
    reset_lines()
    ast = second_analysis(data)
    symbol_table_aux.clear()
    function_table.clear()
    symbol_table.clear()
    return results, ast

# Pruebas
data = '''
# Inicialización de variables
ITEM health = 100;
ITEM enemyHealth = 150;

# Definición de función
CODEC attack() {
    enemyHealth = enemyHealth - 20;
    PRINT("Vida del enemigo reducida a: ");
    PRINT(enemyHealth);
    SCAN (enemyHealth <= 0) {
        PRINT("Enemigo eliminado");
    }
}

# Bucle de ataque
PATROL (enemyHealth > 0) {
    SUMMON attack();
}

'''


