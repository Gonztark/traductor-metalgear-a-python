import ply.lex as lex

reserved = {
    'SCAN': 'IF', 
    'PATROL': 'WHILE', 
    'CODEC': 'FUNCTION', 
    'QUEST': 'FOR', 
    'SUMMON': 'CALL', 
    'EXECUTE': 'DO', 
    'ITEM': 'VAR',
    'PRINT': 'PRINT',  
    'READ': 'READ',
    'RETURN': 'RETURN',
    'EVADE': 'ELSE'
}

tokens = list(reserved.values()) + [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'NE', 'LT', 'LTE', 'GT', 'GTE', 'EQ',
    'LPARENT', 'RPARENT', 'COMMA', 'SEMICOLON',
    'DOT', 'STRING','COMMENT', 'LBRACE', 'RBRACE'
]

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# tokens de operaciones
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='
t_EQ = r'=='
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'
t_LBRACE = r'\{'
t_RBRACE = r'\}'


# Cadenas de texto
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Eliminar las comillas dobles
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'ID')  
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# Comentarios
def t_COMMENT(t):
    r'\#.*'
    pass  

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter no reconocido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def reset_lines():
    lexer.lineno = 1

def analizar_lexico(texto):
    lexer.input(texto)
    resultado = ""
    while True:
        tok = lexer.token()
        if not tok:
            break 
        resultado += str(tok) + "\n"
    return resultado



