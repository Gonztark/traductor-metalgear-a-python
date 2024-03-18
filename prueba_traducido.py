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
        append_result(f"Error semántico: La función '{function_name}' no ha sido declarada.")
        p[0] = {'type': 'undefined_function_call', 'name': function_name, 'arguments': p[4]}


# Inicialización de variables
ITEM health = 100;
ITEM enemyHealth = 150;

# Definición de función
CODEC attack(ITEM damage) {
    enemyHealth = enemyHealth - damage;
    PRINT("Vida del enemigo reducida a: ");
    PRINT(enemyHealth);
    SCAN (enemyHealth <= 0) {
        PRINT("Enemigo eliminado");
    }
}

# Bucle de ataque
PATROL (enemyHealth > 0) {
    SUMMON attack(25);
}


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
                    print(provided_args[1]['value'])
                    print("WAAASSAAAAAAAAA")
        p[0] = {'type': 'function_call', 'name': function_name, 'arguments': provided_args}
    else:
        append_result(f"Error semántico: La función '{function_name}' no ha sido declarada.")
        print(f"Error semántico: La función '{function_name}' no ha sido declarada.")
        p[0] = {'type': 'undefined_function_call', 'name': function_name, 'arguments': p[4]}
