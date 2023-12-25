%include "io.inc"

section .data
	ZEROS equ 0x0
	FALSE equ 0x0
	TRUE equ 0x3f800000
	TMP dd 0.0
	RES dd ZEROS
	ii1 dd ZEROS
	aa1 dd ZEROS

section .text
global main
main:
	mov ebp, esp
	mov dword[ii1], 0x3F800000
M0:
	finit
	fld dword[ii1]
	mov dword[TMP], 0x41200000
	fld dword[TMP]
	fcomi
	jz END0
	mov dword[aa1], 0x41100000
	finit
	fld dword[ii1]
	mov dword[TMP], 0x3F800000
	fld dword[TMP]
	fadd
	fstp dword[RES]
	mov eax, dword[RES]
	mov dword[ii1], eax
	jmp M0
END0:
	PRINT_HEX 4, aa1
	NEWLINE
	ret