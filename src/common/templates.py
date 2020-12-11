# -*- coding: utf-8 -*-
"""Templates

Declares global templates such as email bodies.
"""

_EMAIL_DEFAULT_HEAD = """
<meta charset="UTF-8">
<html>
  <body style="font-family: 'Courier New', Courier, monospace; font-size:12">
    <div>
      <!-- title -->
      <p><b>{}</b></p>
"""
_EMAIL_ADVERTISING_HEAD = """
<meta charset="UTF-8">
<html>
  <body style="font-family: 'Courier New', Courier, monospace; font-size:12">
    <div>
      <!-- title -->
      <p><b>{}</b></p>

      <p><span>Olá, temos vagas abertas para alguns cursos do FIT Tech Academy e gostaríamos que uma divulgação para elas fosse incluída no próximo comunicado.</span></p>
      <p><span>Um arquivo de imagem com as artes para cada curso estão anexos à mensagem, seguem detalhes de quais cursos e quantas vagas temos disponíveis.</span></p>
"""
_EMAIL_DEFAULT_TAIL = """
      <!-- horizontal line -->
      <div><hr></div>

      <!-- end of report -->
      <p><b><span>FIM</span></b></p>
    </div>
  </body>
</html>
"""
_EMAIL_DEFAULT_EMPTY_BODY = """
      <!-- horizontal line -->
      <div><hr></div>

      <!-- nothing to show -->
      <p><span>Nenhum evento a reportar.</span></p>
"""


def compile_list_section(list_entries=None):
  list_section = ""
  if list_entries:
    list_body = [
      f"<li><span>{entry}&#62;</span></li>"
      for entry in list_entries
    ]
    list_section = "\n        ".join(list_body)
    f"<ul>\n      {list_section}\n      </ul>"

  return list_section


def get_email_report_body_entry(
  event_name='',
  teacher='',
  start_date='',
  days_to_start='',
  total_spots='',
  open_spots='',
  open_percentage='',
  confirmations='',
  tentatives='',
  tentative_list=None,
  canceled='',
  canceled_list=None,
  pending='',
  **kwargs
):
  """Retrieve Email Report

  Returns a custom HTML formatted email report "section" for a given event.
  """

  pending_canceling_section = ""    
  if canceled_list:
    pending_canceling_section = "<b><span style='color:#ED7D31; font-size:11;'>**pendente cancelamento no Sympla</span></b>"

  return f"""
      <!-- horizontal line and newline -->
      <div><hr></div>

      <!-- class name -->
      <p><b><span>Turma: </span></b> <span>{event_name}</span></p>

      <!-- teacher -->
      <p><b><span>Professor: </span></b> <span>{teacher}</span></p>

      <!-- start date -->
      <p><b><span>Data de Início: </span></b> <span>{start_date}</span></p>

      <!-- days remaining to course start and open slots -->
      <p><b><u><span style='color:#ED7D31'>Faltam {days_to_start} dias para o início das aulas</span></u></b></p>
      <p><b>
        <u><span>Vagas Disponíveis: {open_spots}</span></u>
        <span style='color:#ABABAB; font-size:11;'> **{open_percentage}% de vagas abertas</span>
      </b></p>

      <!-- newline -->
      <p>&nbsp;</p>

      <!-- inscriptions quantity -->
      <p><b><span>Inscritos: </span></b><span>({confirmations}/{total_spots})</span></p>

      <!-- tentatives quantity -->
      <p><b><span>Tentativas: </span></b><span>({tentatives}/{total_spots})</span></p>
      <!-- tentatives list -->
      {compile_list_section(tentative_list)}

      <!-- canceled quantity -->
      <p>
        <b><span>Cancelados: </span></b>
        <span>({canceled}/{total_spots})</span>
        {pending_canceling_section}
      </p>
      <!-- canceled list -->
      {compile_list_section(canceled_list)}

      <!-- pending quantity -->
      <p><b><span>Pendentes: </span></b><span>({pending}/{total_spots})</span></p>
  """


def get_email_ad_body_entry(
  event_name='',
  start_date='',
  open_spots='',
  event_url='',
  **kwargs
):
  return f"""
      <!-- horizontal line -->
      <div><hr></div>

      <!-- class name -->
      <p><b><span>Turma: </span></b> <span>{event_name}</span></p>

      <!-- start date -->
      <p><b><span>Data de Início: </span></b> <span>{start_date}</span></p>

      <!-- open slots -->
      <p><b><span>Vagas Disponíveis: </span></b> <span>{open_spots}</span></p>

      <!-- art -->
      <p><b><span>Onde se Cadastrar: </span></b> <span>{event_url}</span></p>

      <!-- art -->
      <p><b><span>Anexo: </span></b> <span>{event_name}.png</span></p>
  """



_EMAIL = {
  "meeting_request": {
    "body": "Prezados, Segue meeting para nossa aula {} no dia/hora {}, bom curso a todos! Abs, {}"
  },
  "report": {
    "subject": "[TAMS] - REQUISIÇÃO DE STATUS",
    "head": _EMAIL_DEFAULT_HEAD.format("REQUISIÇÃO DE STATUS DAS TURMAS"),
    "tail": _EMAIL_DEFAULT_TAIL,
    "body": get_email_report_body_entry,
    "attach_art"   : False,
    "force_trigger": True
  },
  "alert_default": {
    "subject": "[TAMS][Alerta] 7 DIAS ANTES DO EVENTO",
    "head": _EMAIL_DEFAULT_HEAD.format("ALERTA PADRÃO - 7 DIAS ANTES DO EVENTO"),
    "tail": _EMAIL_DEFAULT_TAIL,
    "body": get_email_report_body_entry,
    "attach_art"   : False,
    "force_trigger": False
  },
  "alert_critical": {
    "subject": "[TAMS][CRITICAL] 3 DIAS ANTES DO EVENTO",
    "head": _EMAIL_DEFAULT_HEAD.format("ALERTA CRÍTICO - 3 DIAS ANTES DO EVENTO"),
    "tail": _EMAIL_DEFAULT_TAIL,
    "body": get_email_report_body_entry,
    "attach_art"   : False,
    "force_trigger": False
  },
  "advertising": {
    "subject": "[Divulgação] Favor incluir no próximo comunicado",
    "head": _EMAIL_ADVERTISING_HEAD.format("PEDIDO AUTOMÁTICO DE DIVULGAÇÃO"),
    "tail": _EMAIL_DEFAULT_TAIL,
    "body": get_email_ad_body_entry,
    "attach_art"   : True,
    "force_trigger": False
  }
}