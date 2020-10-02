# Trabalho prático de Programação Matemática

### Parâmetros

* **Horários disponíveis**: os intervalos que a pessoa realiza atividades todos os dias, 7h às 20h na segunda, por exemplo.
* **Horários ocupados**: os horários em que a pessoa tem atividades fixas que não podem ser alteradas.
* **Atividades**: as atividades que precisam ser alocadas durante a semana, contendo carga horária semanal, dias da semana que a atividade precisa ser realizada (se houver), carga horária mínima consecutiva e se a atividade precisa ser realizada antes de algum horário ocupado.
* **Horários de refeições**: períodos de refeições que a pessoa prefere, um exemplo seria café da manhã, que deve acontecer entre 7h e 9h, e deve ter duração mínima de 30 minutos.

### Objetivo

Encontrar uma designinação de atividades durante a semana que maximize o tempo ocioso.

#### Restrições

* Duas tarefas não podem ocupar o mesmo horário;
* As tarefas têm que estar dentro do horário disponível;
* As tarefas não podem ser alocadas nos horários ocupados;
* Algumas tarefas devem ser alocadas antes de um determinado horário ocupado;
* As tarefas têm carga horária mínima consecutiva;
* Os horários disponíveis para refeições deve ser respeitado.

### Execução

```
pip3 install openpyxl (apenas apra gerar agenda)
python3 main.py Instancias/instancia_1.txt (executa a heurística)
python3 model.py Instancias/instancia_2.txt (executa o modelo)
```

### [Relatório e Modelo](https://drive.google.com/file/d/1bRkhKKpwPliild8RsDrgolwjNAxXPJvx/view?usp=sharing)
