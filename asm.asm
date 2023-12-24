%include "io.inc"

section .data
	ZEROS equ 0x0
	FALSE equ 0x0
	TRUE equ 0x3f800000
	TMP dd 0.0
	RES dd ZEROS
	kk1 dd ZEROS
	kk2 dd ZEROS
	bb1 dd ZEROS
	bb2 dd ZEROS
	xx1 dd ZEROS
	yy1 dd ZEROS
	tm1 dd ZEROS
	sm1 dd ZEROS
	pr1 dd ZEROS
	eq1 dd ZEROS
	eq2 dd ZEROS

section .text
global main
main:
	mov ebp, esp
	GET_HEX 4, kk1
	GET_HEX 4, bb1
	GET_HEX 4, kk2
	GET_HEX 4, bb2
	finit
	fld dword[kk1]
	fld dword[kk2]
	fcomi
	jz label0
	mov dword[RES], FALSE
	jmp label1
label0:
	mov dword[RES], TRUE
label1:
	mov eax, dword[RES]
	mov dword[eq1], eax
	finit
	fld dword[bb1]
	fld dword[bb2]
	fcomi
	jz label2
	mov dword[RES], FALSE
	jmp label3
label2:
	mov dword[RES], TRUE
label3:
	mov eax, dword[RES]
	mov dword[eq2], eax
	mov eax, dword[eq1]
	and eax, dword[eq2]
	mov dword[RES], eax
	finit
	fld dword[RES]
	mov dword[TMP], 0x00000000
	fld dword[TMP]
	fcomi
	jnz label4
	jmp M0
label4:
	mov dword[sm1], TRUE
	jmp END0
M0:
	finit
	fld dword[eq1]
	mov dword[TMP], TRUE
	fld dword[TMP]
	fcomi
	jz label5
	mov dword[RES], FALSE
	jmp label6
label5:
	mov dword[RES], TRUE
label6:
	finit
	fld dword[RES]
	mov dword[TMP], 0x00000000
	fld dword[TMP]
	fcomi
	jnz label7
	jmp M1
label7:
	mov dword[pr1], TRUE
	jmp END0
M1:
	finit
	fld dword[bb2]
	fld dword[bb1]
	fsub
	fstp dword[RES]
	mov eax, dword[RES]
	mov dword[xx1], eax
	finit
	fld dword[kk1]
	fld dword[kk2]
	fsub
	fstp dword[RES]
	mov eax, dword[RES]
	mov dword[tm1], eax
	finit
	fld dword[xx1]
	fld dword[tm1]
	fdiv
	fstp dword[RES]
	mov eax, dword[RES]
	mov dword[xx1], eax
	finit
	fld dword[kk1]
	fld dword[xx1]
	fmul
	fstp dword[RES]
	mov eax, dword[RES]
	mov dword[yy1], eax
	finit
	fld dword[yy1]
	fld dword[bb1]
	fadd
	fstp dword[RES]
	mov eax, dword[RES]
	mov dword[yy1], eax
END0:
	PRINT_HEX 4, xx1
	NEWLINE
	PRINT_HEX 4, yy1
	NEWLINE
	ret