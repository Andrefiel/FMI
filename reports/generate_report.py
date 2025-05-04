from fpdf import FPDF

def generate_report(filename, logo_path, start_date, end_date):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    if logo_path:
        pdf.image(logo_path, 10, 8, 33)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Monitoramento", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Início: {start_date}  |  Fim: {end_date}", ln=True)

    # Adicionar mais detalhes sobre as ações de arquivos monitoradas aqui

    pdf.output(filename)
