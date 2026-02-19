import pdfplumber
import re
import json
import os
import glob

def extrair_dados_fatura(caminho_pdf):
    dados_extraidos = {
        "Titular (Nome)": None,
        "Documento (CPF/CNPJ)": None,
        "Número da Instalação": None,
        "Valor a Pagar (R$)": None,
        "Data de Vencimento": None,
        "Mês Referência": None,
        "Consumo (kWh)": None,
        "Saldo Acumulado (kWh)": None,
        "Iluminação Pública (R$)": None
    }

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            texto_completo = ""
            for pagina in pdf.pages:
                texto_extraido = pagina.extract_text()
                if texto_extraido:
                    texto_completo += texto_extraido + "\n"

            if not texto_completo:
                return {"Erro": "Nenhum texto encontrado."}

           # 1. Nome do Titular e CPF (Mantemos igual)
            linhas = texto_completo.split('\n')
            for linha in linhas[:15]:
                if "JOAO NEVES" in linha:
                    dados_extraidos["Titular (Nome)"] = "JOAO NEVES"
                    break

            match_cpf = re.search(r'CPF\s*:?\s*([\d\.\-]+)', texto_completo, re.IGNORECASE)
            if match_cpf:
                dados_extraidos["Documento (CPF/CNPJ)"] = match_cpf.group(1)

            # 3. Número da Instalação (Pula até 30 caracteres até achar 8 a 11 dígitos)
            match_inst = re.search(r'(?:Nº DA INSTALAÇÃO|INSTALAÇÃO)[\s\S]{0,30}?(\d{8,11})', texto_completo, re.IGNORECASE)
            if match_inst:
                dados_extraidos["Número da Instalação"] = match_inst.group(1)

            # 4. Valor a Pagar (Busca as palavras-chave e pula caracteres até achar o formato de moeda ex: 418,02)
            match_valor = re.search(r'(?:Valor a pagar|Total a pagar|TOTAL A PAGAR|Total Consolidado)[\s\S]{0,40}?(\d{1,5}[,\.]\d{2})', texto_completo, re.IGNORECASE)
            if match_valor:
                dados_extraidos["Valor a Pagar (R$)"] = match_valor.group(1).replace('.', ',')

            # 5. Data de Vencimento
            match_vencimento = re.search(r'Vencimento[\s\S]{0,30}?(\d{2}/\d{2}/\d{4})', texto_completo, re.IGNORECASE)
            if match_vencimento:
                dados_extraidos["Data de Vencimento"] = match_vencimento.group(1)

            # 6. Mês de Referência
            match_mes = re.search(r'(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)/\d{4}', texto_completo, re.IGNORECASE)
            if match_mes:
                dados_extraidos["Mês Referência"] = match_mes.group(0)

            # 7. Saldo Acumulado (Geração) - Com a correção de formatação
            match_saldo_cemig = re.search(r'SALDO ATUAL DE GERAÇÃO:[\s\S]{0,20}?([\d\,\.]+)\s*kWh', texto_completo, re.IGNORECASE)
            match_saldo_cpfl = re.search(r'Saldo em Energia[\s\S]{0,50}?([\d\,\.]+)\s*kWh', texto_completo, re.IGNORECASE)
            
            saldo_bruto = match_saldo_cemig.group(1) if match_saldo_cemig else (match_saldo_cpfl.group(1) if match_saldo_cpfl else None)
            
            if saldo_bruto:
                if ',' in saldo_bruto:
                    inteiro, decimal = saldo_bruto.split(',')
                    dados_extraidos["Saldo Acumulado (kWh)"] = f"{inteiro},{decimal[:2]}"
                else:
                    dados_extraidos["Saldo Acumulado (kWh)"] = saldo_bruto

            # 8. Contribuição de Iluminação Pública
            match_ilum = re.search(r'(?:llum Publica|IP-CIP)[\s\S]{0,40}?(\d{1,4}[,\.]\d{2})', texto_completo, re.IGNORECASE)
            if match_ilum:
                dados_extraidos["Iluminação Pública (R$)"] = match_ilum.group(1).replace('.', ',')
                
            # 9. Consumo em kWh
            match_consumo = re.search(r'(?:Energia Elétrica|Energia Ativa)[\s\S]{0,40}?kWh[\s\S]{0,30}?(\d+[\.,]?\d*)', texto_completo, re.IGNORECASE)
            if match_consumo:
                dados_extraidos["Consumo (kWh)"] = match_consumo.group(1)

    except Exception as e:
        return {"Erro": str(e)}

    return dados_extraidos

if __name__ == "__main__":
    pasta_pdfs = "." 
    arquivos_pdf = glob.glob(os.path.join(pasta_pdfs, "*.pdf"))
    
    if not arquivos_pdf:
        print("⚠️ Nenhum arquivo PDF encontrado na pasta.")
    else:
        for arquivo in arquivos_pdf:
            nome_arquivo = os.path.basename(arquivo)
            print(f"\n{'='*50}")
            print(f"📄 ARQUIVO: {nome_arquivo}")
            print(f"{'='*50}")
            
            resultado = extrair_dados_fatura(arquivo)
            print(json.dumps(resultado, indent=4, ensure_ascii=False))