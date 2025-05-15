section .data
    fmt_input_count db "%d", 0        ; Формат для ввода числа
    fmt_input_str db "%s", 0          ; Формат для ввода строки
    fmt_output_matrix db "%s", 10, 0  ; Формат для вывода строки с переносом строки
    replacement db "7890", 0          ; Константа для замены
    percent_replacement db "%%%%", 0  ; Константа для замены процентами

section .bss
    rows resd 1                       ; Количество строк
    cols resd 1                       ; Количество символов в строке
    array resb 10*15                  ; Массив для хранения строк (max 10 строк по 15 символов)

section .text
    extern scanf, printf
    global main

main:
    push rbp
    mov rbp, rsp
    sub rsp, 32                       ; Выделяем место в стеке

    ; Ввод количества строк
    lea rdi, [fmt_input_count]
    lea rsi, [rows]
    xor eax, eax
    call scanf

    ; Ввод количества символов в строке
    lea rdi, [fmt_input_count]
    lea rsi, [cols]
    xor eax, eax
    call scanf

    ; Ввод строк
    mov ecx, [rows]
    mov rbx, 0                        ; Индекс текущей строки
    
input_loop:
    cmp ecx, 0
    je input_done
    
    ; Вычисляем адрес текущей строки
    mov rax, rbx
    mul dword [cols]
    lea rsi, [array + rax]
    
    ; Вводим строку
    lea rdi, [fmt_input_str]
    xor eax, eax
    call scanf
    
    inc rbx
    dec ecx
    jmp input_loop

input_done:
    ; Вызов процедуры обработки массива через стек
    mov edx, [cols]                   ; Третий параметр - количество символов в строке
    push rdx
    mov esi, [rows]                   ; Второй параметр - количество строк
    push rsi
    lea rdi, [array]                  ; Первый параметр - адрес массива
    push rdi
    call process_array
    add rsp, 24                       ; Очищаем стек
    
    ; Вывод результата
    mov ecx, [rows]
    mov rbx, 0                        ; Индекс текущей строки
    
output_loop:
    cmp ecx, 0
    je output_done
    
    ; Вычисляем адрес текущей строки
    mov rax, rbx
    mul dword [cols]
    lea rsi, [array + rax]
    
    ; Выводим строку
    lea rdi, [fmt_output_matrix]
    xor eax, eax
    call printf
    
    inc rbx
    dec ecx
    jmp output_loop

output_done:
    ; Завершение программы
    xor eax, eax
    leave
    ret

; Процедура обработки массива
; Параметры через стек: 
; [rbp+16] - адрес массива
; [rbp+24] - количество строк
; [rbp+32] - количество символов в строке
process_array:
    push rbp
    mov rbp, rsp
    sub rsp, 32                       ; Выделяем место в стеке
    
    ; Локальная строковая переменная "1234"
    mov byte [rbp-16], '1'
    mov byte [rbp-15], '2'
    mov byte [rbp-14], '3'
    mov byte [rbp-13], '4'
    mov byte [rbp-12], 0
    
    ; Получаем параметры из стека
    mov r12, [rbp+16]                 ; r12 = адрес массива
    mov r13d, [rbp+24]                ; r13d = количество строк
    mov r14d, [rbp+32]                ; r14d = количество символов в строке
    
    ; Обрабатываем каждую строку
    mov ecx, r13d                     ; ecx = количество строк
    mov rbx, 0                        ; Индекс текущей строки
    
process_loop:
    cmp ecx, 0
    je process_done
    
    ; Вычисляем адрес текущей строки
    mov rax, rbx
    mul r14d
    lea rdi, [r12 + rax]
    
    ; Ищем "1234" в строке
    lea rsi, [rbp-16]                 ; rsi = адрес локальной переменной "1234"
    call find_substring
    
    ; Если найдено (rax != 0), заменяем на "7890"
    cmp rax, 0
    je not_found
    
    ; Заменяем "1234" на "7890"
    mov rdi, rax                      ; rdi = адрес найденной подстроки
    lea rsi, [replacement]            ; rsi = адрес константы "7890"
    mov edx, 4                        ; длина замены
    call replace_substring
    jmp next_string
    
not_found:
    ; Если не найдено, заменяем первые 4 символа на "%%%%"
    mov rax, rbx
    mul r14d
    lea rdi, [r12 + rax]
    
    ; Проверяем, что строка имеет хотя бы 1 символ
    mov al, byte [rdi]
    cmp al, 0
    je next_string
    
    ; Заменяем первые 4 символа
    lea rsi, [percent_replacement]    ; rsi = адрес константы "%%%%" 
    mov edx, 4                        ; длина замены
    call replace_prefix
    
next_string:
    inc rbx
    dec ecx
    jmp process_loop
    
process_done:
    leave
    ret

; Функция поиска подстроки
; rdi - строка, rsi - подстрока для поиска
; возвращает rax - адрес найденной подстроки или 0, если не найдено
find_substring:
    push rbp
    mov rbp, rsp
    
    ; Проверяем каждый символ
find_loop:
    mov al, byte [rdi]
    cmp al, 0
    je not_found_substr             ; Конец строки, подстрока не найдена
    
    ; Сравниваем текущую позицию с подстрокой
    mov r9, rdi                     ; r9 = текущая позиция в строке
    mov r10, rsi                    ; r10 = начало подстроки
    
compare_loop:
    mov al, byte [r10]
    cmp al, 0
    je found_substr                 ; Конец подстроки, подстрока найдена
    
    mov bl, byte [r9]
    cmp bl, 0
    je not_found_substr             ; Конец строки, подстрока не найдена
    
    cmp al, bl
    jne no_match                    ; Символы не совпали
    
    inc r9
    inc r10
    jmp compare_loop
    
no_match:
    inc rdi
    jmp find_loop
    
found_substr:
    mov rax, rdi                    ; Возвращаем адрес найденной подстроки
    jmp find_substring_done
    
not_found_substr:
    xor rax, rax                    ; Возвращаем 0 (не найдено)
    
find_substring_done:
    leave
    ret

; Функция замены подстроки
; rdi - адрес подстроки для замены, rsi - новая подстрока, edx - длина новой подстроки
replace_substring:
    push rbp
    mov rbp, rsp
    
    ; Копируем новую подстроку
    mov ecx, edx
    
replace_loop:
    mov al, byte [rsi]
    mov byte [rdi], al
    inc rsi
    inc rdi
    dec ecx
    jnz replace_loop
    
    leave
    ret

; Функция замены префикса строки
; rdi - адрес строки, rsi - новый префикс, edx - длина нового префикса
replace_prefix:
    push rbp
    mov rbp, rsp
    
    ; Копируем новый префикс
    mov ecx, edx
    
replace_prefix_loop:
    mov al, byte [rsi]
    mov byte [rdi], al
    inc rsi
    inc rdi
    dec ecx
    jnz replace_prefix_loop
    
    leave
    ret