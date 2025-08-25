from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import pandas as pd
from  datetime import datetime
import os

def export_to_excel(expenses,expenses_file, language=None):
    export_folder = "exports"

    df = pd.DataFrame(expenses)
    df['total'] = df['quantity'] * df['value']
    df['date'] = pd.to_datetime(df['date'])

    filename = f"{expenses_file}_export_{datetime.now().strftime('%d%m%Y_%H%M%S')}.xlsx"
    filepath = os.path.join(export_folder, filename)

    df.to_excel(filepath, index=False)

    print(f"{language['excel_export_success']} {filename}")

def generate_pdf_report(expenses, output_folder="reports",language=None):
    if not expenses:
        print(language['error'])
        return

    os.makedirs(output_folder, exist_ok=True)

    report_name = f"{language['pdf_name']}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.pdf"
    report_path = os.path.join(output_folder, report_name)

    df = pd.DataFrame(expenses)

    doc = SimpleDocTemplate(report_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{language['pdf_heading']}</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"{language['pdf_date']} {datetime.now().strftime('%d-%m-%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>{language['pdf_list']}</b>", styles['Heading2']))
    data = [["Data", "Nazwa", "Kategoria", "Ilość", "Wartość (PLN)"]]
    for _, row in df.iterrows():
        data.append([row['date'], row['item_name'], row['category'], row['quantity'], row['value']])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    story.append(table)
    story.append(Spacer(1, 20))

    total = df['value'].sum()
    story.append(Paragraph(f"<b>{language['pdf_wrapup']}</b>", styles['Heading2']))
    story.append(Paragraph(f"{language['pdf_summary']} <b>{total:.2f} PLN</b>", styles['Normal']))

    doc.build(story)

    print(f" {language['pdf_filepath']} {report_path}")
    return report_path
