section .data
    yes_msg db "Yes", 0
    no_msg db "No", 0
    
section .bss
    buffer resb 256      ; Буфер для ввода строки
    stack resb 100       ; Стек для проверки скобок
    stack_ptr resd 1     ; Указатель на вершину стека
    
section .text
    global _start
    
_start:
    ; Обнуляем указатель стека
    mov dword [stack_ptr], 0
    
    ; Читаем строку с помощью прерывания
    mov eax, 3          ; sys_read
    mov ebx, 0          ; stdin
    mov ecx, buffer     ; буфер для строки
    mov edx, 255        ; максимальная длина
    int 0x80
    
    ; Проверяем скобочную запись
    mov esi, buffer     ; ESI указывает на начало строки
    
parse_loop:
    mov al, [esi]       ; Берем текущий символ
    
    ; Проверяем конец ввода (пробел)
    cmp al, ' '
    je check_stack_empty
    
    ; Проверяем открывающие скобки
    cmp al, '('
    je push_to_stack
    cmp al, '['
    je push_to_stack
    cmp al, '{'
    je push_to_stack
    
    ; Проверяем закрывающие скобки
    cmp al, ')'
    je check_round_bracket
    cmp al, ']'
    je check_square_bracket
    cmp al, '}'
    je check_curly_bracket
    
    ; Переходим к следующему символу (если это не скобка)
    inc esi
    jmp parse_loop
    
push_to_stack:
    ; Добавляем открывающую скобку в стек
    mov ebx, [stack_ptr]
    mov [stack + ebx], al
    inc dword [stack_ptr]
    inc esi
    jmp parse_loop
    
check_round_bracket:
    ; Проверяем соответствие для ')'
    cmp dword [stack_ptr], 0
    je invalid_expression  ; Стек пуст - ошибка
    
    mov ebx, [stack_ptr]
    dec ebx
    cmp byte [stack + ebx], '('
    jne invalid_expression  ; Несоответствие скобок
    
    dec dword [stack_ptr]  ; Удаляем из стека
    inc esi                ; Следующий символ
    jmp parse_loop
    
check_square_bracket:
    ; Проверяем соответствие для ']'
    cmp dword [stack_ptr], 0
    je invalid_expression
    
    mov ebx, [stack_ptr]
    dec ebx
    cmp byte [stack + ebx], '['
    jne invalid_expression
    
    dec dword [stack_ptr]
    inc esi
    jmp parse_loop
    
check_curly_bracket:
    ; Проверяем соответствие для '}'
    cmp dword [stack_ptr], 0
    je invalid_expression
    
    mov ebx, [stack_ptr]
    dec ebx
    cmp byte [stack + ebx], '{'
    jne invalid_expression
    
    dec dword [stack_ptr]
    inc esi
    jmp parse_loop
    
check_stack_empty:
    ; Проверяем, что стек пуст (все скобки закрыты)
    cmp dword [stack_ptr], 0
    jne invalid_expression
    
    ; Выражение правильное - выводим "Yes"
    mov eax, 4          ; sys_write
    mov ebx, 1          ; stdout
    mov ecx, yes_msg    ; сообщение
    mov edx, 3          ; длина сообщения
    int 0x80
    jmp exit
    
invalid_expression:
    ; Выражение неправильное - выводим "No"
    mov eax, 4          ; sys_write
    mov ebx, 1          ; stdout
    mov ecx, no_msg     ; сообщение
    mov edx, 2          ; длина сообщения
    int 0x80
    
exit:
    ; Завершение программы
    mov eax, 1          ; sys_exit
    xor ebx, ebx        ; код возврата 0
    int 0x80