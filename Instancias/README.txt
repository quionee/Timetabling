n_quantidades_de_dias_disponiveis
dia_1 hora_inicial_1 hora_final_1
...
dia_n hora_inicial_n hora_final_n
m_quantidades_de_horarios_ocupados
dia_ocupado_1 j_quantidade_de_horarios_ocupados_do_dia hora_inicial_1 hora_final_1 ... hora_inicial_j hora_final_j
...
dia_ocupado_m j_quantidade_de_horarios_ocupados_do_dia hora_inicial_1 hora_final_1 ... hora_inicial_j hora_final_j
p_quantidades_de_atividades
nome_atividade_1 carga_horaria_semanal i_qtd_dias_possiveis dia_possivel_1 ... dia_possivel_i carga_horaria_consecutiva id_requisito dia_do_requisito hora_do_requisito
...
nome_atividade_p carga_horaria_semanal i_qtd_dias_possiveis dia_possivel_1 ... dia_possivel_i carga_horaria_consecutiva id_requisito dia_do_requisito hora_do_requisito
r_quantidades_de_refeicoes
nome_refeicao_1 limite_inferior_1 limite_superior_1 duracao
...
nome_refeicao_r limite_inferior_r limite_superior_r duracao

* id_requisito == -1, dia_do_requisito & hora_do_requisito == ''
