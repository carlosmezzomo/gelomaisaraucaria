import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import datetime
import math

class CalculadoraGelo:
    def __init__(self, root):
        self.root = root
        self.root.title("GELO+ Calculadora")
        self.root.geometry("400x700")  # Tamanho reduzido
        
        # Definindo cores do tema
        self.cor_principal = "#0066cc"
        self.cor_secundaria = "#e6f3ff"
        self.cor_texto = "#333333"
        self.cor_destaque = "#ff9900"
        
        # Configurando o fundo
        self.root.configure(bg=self.cor_secundaria)
        
        # Frame principal
        main_frame = tk.Frame(root, bg=self.cor_secundaria, padx=15, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        # Carregando o logo
        try:
            self.logo_path = r"C:\Users\Carlo\OneDrive\Área de Trabalho\Calculadora GELO+\img\gelo+.jpeg"
            logo_image = Image.open(self.logo_path)
            logo_image = logo_image.resize((200, 100))  # Logo menor
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(main_frame, image=self.logo_photo, bg=self.cor_secundaria)
            logo_label.pack(pady=15)
        except Exception as e:
            print(f"Erro ao carregar o logo: {e}")
            self.logo_path = ""  # Path vazio em caso de erro

        # Frame para entrada de dados
        input_frame = tk.Frame(main_frame, bg=self.cor_secundaria, pady=15)
        input_frame.pack(fill='x')

        # Entrada da litragem
        tk.Label(
            input_frame, 
            text="Litragem Total Necessária:", 
            font=("Arial", 10, "bold"),
            bg=self.cor_secundaria,
            fg=self.cor_texto
        ).pack(pady=3)
        
        self.litragem = ttk.Entry(
            input_frame,
            font=("Arial", 10),
            justify='center'
        )
        self.litragem.pack(pady=3, ipady=3, ipadx=20)
        self.litragem.bind('<KeyRelease>', self.calcular_automatico)  # Adiciona evento de atualização

        # Frame para temperatura
        temp_frame = tk.LabelFrame(
            main_frame,
            text="Temperatura Ambiente",
            font=("Arial", 10, "bold"),
            bg=self.cor_secundaria,
            fg=self.cor_texto,
            padx=10,
            pady=5
        )
        temp_frame.pack(pady=10, padx=20, fill='x')

        # Frame para temperaturas mínima e máxima
        temp_input_frame = tk.Frame(temp_frame, bg=self.cor_secundaria)
        temp_input_frame.pack(fill='x', pady=5)

        # Temperatura Mínima
        tk.Label(
            temp_input_frame,
            text="Mínima (°C):",
            font=("Arial", 9),
            bg=self.cor_secundaria,
            fg=self.cor_texto
        ).pack(side='left', padx=(0,10))

        self.temp_min = ttk.Entry(
            temp_input_frame,
            font=("Arial", 9),
            width=6,
            justify='center'
        )
        self.temp_min.pack(side='left', padx=(0,20))
        self.temp_min.bind('<KeyRelease>', self.calcular_automatico)

        # Temperatura Máxima
        tk.Label(
            temp_input_frame,
            text="Máxima (°C):",
            font=("Arial", 9),
            bg=self.cor_secundaria,
            fg=self.cor_texto
        ).pack(side='left', padx=(0,10))

        self.temp_max = ttk.Entry(
            temp_input_frame,
            font=("Arial", 9),
            width=6,
            justify='center'
        )
        self.temp_max.pack(side='left')
        self.temp_max.bind('<KeyRelease>', self.calcular_automatico)

        # Valores padrão
        self.temp_min.insert(0, "0")
        self.temp_max.insert(0, "30")

        # Frame para umidade e exposição solar
        ambiente_frame = tk.LabelFrame(
            main_frame,
            text="Condições Ambientais",
            font=("Arial", 10, "bold"),
            bg=self.cor_secundaria,
            fg=self.cor_texto,
            padx=10,
            pady=5
        )
        ambiente_frame.pack(pady=10, padx=20, fill='x')

        # Campo para umidade
        umidade_input_frame = tk.Frame(ambiente_frame, bg=self.cor_secundaria)
        umidade_input_frame.pack(fill='x', pady=5)

        # Umidade Mínima
        tk.Label(
            umidade_input_frame,
            text="Umidade Mín (%):",
            font=("Arial", 9),
            bg=self.cor_secundaria,
            fg=self.cor_texto
        ).pack(side='left', padx=(0,10))

        self.umidade_min = ttk.Entry(
            umidade_input_frame,
            font=("Arial", 9),
            width=6,
            justify='center'
        )
        self.umidade_min.pack(side='left', padx=(0,20))
        self.umidade_min.bind('<KeyRelease>', self.calcular_automatico)

        # Umidade Máxima
        tk.Label(
            umidade_input_frame,
            text="Máx (%):",
            font=("Arial", 9),
            bg=self.cor_secundaria,
            fg=self.cor_texto
        ).pack(side='left', padx=(0,10))

        self.umidade_max = ttk.Entry(
            umidade_input_frame,
            font=("Arial", 9),
            width=6,
            justify='center'
        )
        self.umidade_max.pack(side='left')
        self.umidade_max.bind('<KeyRelease>', self.calcular_automatico)

        # Valores padrão para umidade
        self.umidade_min.insert(0, "0")
        self.umidade_max.insert(0, "100")

        # Checkbox para exposição solar
        self.sol_direto = tk.BooleanVar()
        tk.Checkbutton(
            ambiente_frame,
            text="Exposição solar direta",
            variable=self.sol_direto,
            bg=self.cor_secundaria,
            font=("Arial", 9),
            command=self.calcular_automatico
        ).pack(anchor='w')

        # Área de resultados estilizada
        self.resultado_text = tk.Text(
            main_frame,
            height=12,  # Aumentado para acomodar mais informações
            width=40,
            font=("Courier", 9),
            bg="white",
            relief="flat",
            padx=10,
            pady=10
        )
        self.resultado_text.pack(pady=15)

        # Botão de impressão estilizado
        imprimir_btn = tk.Button(
            main_frame,
            text="Imprimir Resultado",
            command=self.imprimir,
            bg=self.cor_destaque,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        imprimir_btn.pack(pady=5)

        # Barra de progresso para o tempo de derretimento
        self.progress_frame = tk.LabelFrame(
            main_frame,
            text="Progresso do Derretimento",
            font=("Arial", 10, "bold"),
            bg=self.cor_secundaria,
            fg=self.cor_texto,
            padx=10,
            pady=5
        )
        self.progress_frame.pack(pady=10, padx=20, fill='x')

        self.progress = ttk.Progressbar(
            self.progress_frame,
            length=300,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        self.progress_label = tk.Label(
            self.progress_frame,
            text="0%",
            font=("Arial", 9),
            bg=self.cor_secundaria,
            fg=self.cor_texto
        )
        self.progress_label.pack()

    def calcular_densidade_gelo(self, temperatura):
        # Densidade do gelo a 0°C é exatamente 0.917 kg/L
        densidade_base = 0.917
        
        if temperatura > 0:
            # A densidade diminui muito levemente com o aumento da temperatura
            # Aproximadamente 0.000005 por grau Celsius para manter mais próximo de 0.917
            fator_temperatura = 1 - (temperatura * 0.000005)
            return densidade_base * fator_temperatura
        return densidade_base  # Retorna exatamente 0.917 para temperaturas ≤ 0°C

    def calcular_tempo_derretimento(self, massa_gelo, temperatura, umidade, sol_direto):
        # Constantes físicas
        calor_fusao = 334  # kJ/kg (calor latente de fusão do gelo)
        calor_especifico = 2.108  # kJ/kg.°C (calor específico do gelo)
        
        # Energia solar (W/m²) - Aumentada significativamente a diferença
        energia_solar_base = 300 if sol_direto else 50  # 6x mais energia com sol direto
        area_superficie = math.pow(massa_gelo / 0.917, 2/3)  # aproximação da área superficial
        
        # Fatores ambientais
        fator_solar = 0.25 if sol_direto else 1.0  # 75% mais rápido com sol direto
        fator_umidade = 1 - (umidade / 100) * 0.2  # Reduz até 20% com umidade alta
        
        # Energia necessária para derreter (kJ)
        energia_fusao_total = massa_gelo * calor_fusao
        energia_aquecimento = massa_gelo * calor_especifico * max(0, temperatura)
        energia_total = energia_fusao_total + energia_aquecimento
        
        # Taxa de transferência de calor (kJ/h)
        taxa_base = energia_solar_base * 3.6 * area_superficie
        taxa_transferencia = taxa_base * fator_solar * fator_umidade
        
        # Ajuste por massa
        if massa_gelo <= 10:
            fator_massa = 1.0
        elif massa_gelo <= 50:
            fator_massa = 1.1
        elif massa_gelo <= 100:
            fator_massa = 1.2
        else:
            fator_massa = 1.3
        
        # Tempo total em horas
        tempo_derretimento = (energia_total / taxa_transferencia) * fator_massa
        
        return max(1, min(tempo_derretimento, 48))

    def get_temperatura_valor(self):
        try:
            temp_min = float(self.temp_min.get())
            temp_max = float(self.temp_max.get())
            temp_media = (temp_min + temp_max) / 2
            
            return {
                'min': temp_min,
                'max': temp_max,
                'media': temp_media
            }
        except ValueError:
            return {
                'min': 25,
                'max': 30,
                'media': 27.5
            }

    def formatar_tempo(self, horas):
        """Converte horas decimais para formato brasileiro de horas e minutos"""
        horas_inteiras = int(horas)
        minutos = int((horas - horas_inteiras) * 60)
        
        if minutos == 0:
            if horas_inteiras == 1:
                return "1 hora"
            return f"{horas_inteiras} horas"
        elif horas_inteiras == 0:
            return f"{minutos} minutos"
        elif horas_inteiras == 1:
            if minutos == 1:
                return "1 hora e 1 minuto"
            return f"1 hora e {minutos} minutos"
        else:
            if minutos == 1:
                return f"{horas_inteiras} horas e 1 minuto"
            return f"{horas_inteiras} horas e {minutos} minutos"

    def get_descricao_temperatura(self, temp, sol_direto=False):
        # Base do tempo ajustada pela exposição solar
        tempo_base = self.calcular_tempo_base(temp)
        if sol_direto:
            tempo_base *= 0.25  # 75% mais rápido com sol direto
        
        if temp >= 30:
            estado = "Derretimento muito rápido"
        elif temp >= 25:
            estado = "Derretimento rápido"
        elif temp >= 18:
            estado = "Derretimento moderado"
        else:
            estado = "Derretimento lento"
            
        tempo_formatado = self.formatar_tempo(tempo_base)
        return f"{estado} ({tempo_formatado} por kg {'com' if sol_direto else 'sem'} exposição solar)"

    def calcular_tempo_base(self, temperatura):
        # Calcula o tempo base por kg para uma determinada temperatura
        if temperatura <= 0:
            return 2.0
        elif temperatura <= 10:
            return 1.5
        elif temperatura <= 20:
            return 1.0
        elif temperatura <= 30:
            return 0.7
        else:
            return 0.5

    def atualizar_progresso(self, tempo_total, tempo_atual=0):
        if tempo_atual <= tempo_total:
            porcentagem = (tempo_atual / tempo_total) * 100
            self.progress['value'] = porcentagem
            self.progress_label.config(text=f"{porcentagem:.1f}%")
            self.root.after(100, lambda: self.atualizar_progresso(tempo_total, tempo_atual + 0.1))

    def get_umidade_valor(self):
        try:
            umidade_min = float(self.umidade_min.get())
            umidade_max = float(self.umidade_max.get())
            
            if not (0 <= umidade_min <= 100 and 0 <= umidade_max <= 100):
                raise ValueError("Umidade deve estar entre 0 e 100")
                
            return (umidade_min + umidade_max) / 2
        except ValueError:
            return 70  # valor padrão

    def calcular_densidade_gelo_novo(self, temperatura):
        # Mantendo consistência com o método principal
        return self.calcular_densidade_gelo(temperatura)

    def calcular_tempo_derretimento_novo(self, massa_gelo, temp_media, umidade, sol_direto):
        densidade_gelo = self.calcular_densidade_gelo_novo(temp_media)
        
        # Fatores ajustando com base na temperatura
        fator_temperatura = 1 + (temp_media - 25) * 0.05
        
        # Ajuste dependendo de exposição solar
        fator_exposicao = 1.5 if sol_direto else 1.0

        # Tempo de derretimento (simplificação)
        tempo_derretimento = massa_gelo / (fator_temperatura * fator_exposicao)
        return tempo_derretimento

    def calcular_automatico(self, event=None):
        try:
            valor = self.litragem.get()
            if not valor:
                self.resultado_text.delete(1.0, tk.END)
                return
                
            volume_solicitado = float(valor)
            
            # Obtém temperaturas e calcula densidade
            temperaturas = self.get_temperatura_valor()
            densidade = self.calcular_densidade_gelo(temperaturas['media'])
            
            # Obtém umidade média
            umidade = self.get_umidade_valor()
            
            # Cálculo do peso total de gelo necessário
            peso_gelo = volume_solicitado * densidade
            
            # Cálculo para cada tipo de saco separadamente
            apenas_sacos_10kg = {
                'quantidade': math.ceil(peso_gelo / 10),
                'peso_total': math.ceil(peso_gelo / 10) * 10
            }
            
            apenas_sacos_3kg = {
                'quantidade': math.ceil(peso_gelo / 3),
                'peso_total': math.ceil(peso_gelo / 3) * 3
            }
            
            apenas_sacos_1kg = {
                'quantidade': math.ceil(peso_gelo),
                'peso_total': math.ceil(peso_gelo)
            }
            
            # Cálculo otimizado (combinação de sacos)
            sacos_10kg = int(peso_gelo // 10)
            resto = peso_gelo % 10
            
            sacos_3kg = int(resto // 3)
            resto = resto % 3
            
            sacos_1kg = math.ceil(resto)

            # Peso total na combinação otimizada
            peso_total_combinado = (sacos_10kg * 10) + (sacos_3kg * 3) + sacos_1kg

            # Calcula tempo total de derretimento baseado na temperatura média
            tempo_derretimento = self.calcular_tempo_derretimento(
                peso_gelo,
                temperaturas['media'],
                umidade,
                self.sol_direto.get()
            )

            # Formata o tempo de derretimento
            tempo_formatado = self.formatar_tempo(tempo_derretimento)

            resultado = f"""
GELO+ - Resultado do Cálculo
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
----------------------------------
Volume desejado: {volume_solicitado:.1f}L
Peso em gelo: {peso_gelo:.1f}Kg
Densidade do gelo: {densidade:.3f}kg/L
Temperatura mín/máx: {temperaturas['min']:.1f}°C / {temperaturas['max']:.1f}°C
Temperatura média: {temperaturas['media']:.1f}°C
Umidade mín/máx: {float(self.umidade_min.get()):.0f}% / {float(self.umidade_max.get()):.0f}%
Umidade média: {umidade:.0f}%
Exposição solar: {'Direta' if self.sol_direto.get() else 'Indireta'}
Estado: {self.get_descricao_temperatura(temperaturas['media'], self.sol_direto.get())}
----------------------------------
Opções de compra:

1. Apenas sacos de 10Kg:
   {apenas_sacos_10kg['quantidade']} sacos
   Total: {apenas_sacos_10kg['peso_total']}Kg

2. Apenas sacos de 3Kg:
   {apenas_sacos_3kg['quantidade']} sacos
   Total: {apenas_sacos_3kg['peso_total']}Kg

3. Apenas sacos de 1Kg:
   {apenas_sacos_1kg['quantidade']} sacos
   Total: {apenas_sacos_1kg['peso_total']}Kg

4. Combinação otimizada:
   Sacos de 10Kg: {sacos_10kg}
   Sacos de 3Kg: {sacos_3kg}
   Sacos de 1Kg: {sacos_1kg}
   Total: {peso_total_combinado:.1f}Kg
----------------------------------
Volume final após derretimento: {volume_solicitado:.1f}L
Tempo estimado de derretimento: {tempo_formatado}
"""
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(1.0, resultado)

            # Atualiza a barra de progresso
            self.atualizar_progresso(tempo_derretimento)

        except ValueError:
            if self.litragem.get() != "":
                self.resultado_text.delete(1.0, tk.END)
                self.resultado_text.insert(1.0, "Por favor, insira um valor válido para a litragem.")

    # Substituindo o método calcular pelo automático
    calcular = calcular_automatico

    def gerar_pagina_impressao(self):
        try:
            # Obtém os dados atuais do cálculo
            volume_solicitado = float(self.litragem.get())
            temperaturas = self.get_temperatura_valor()
            densidade = self.calcular_densidade_gelo(temperaturas['media'])
            umidade = self.get_umidade_valor()
            peso_gelo = volume_solicitado * densidade
            
            # Cálculo dos sacos
            sacos_10kg = int(peso_gelo // 10)
            resto = peso_gelo % 10
            sacos_3kg = int(resto // 3)
            resto = resto % 3
            sacos_1kg = math.ceil(resto)
            
            peso_total_combinado = (sacos_10kg * 10) + (sacos_3kg * 3) + sacos_1kg
            
            # Calcula tempo de derretimento
            tempo_derretimento = self.calcular_tempo_derretimento(
                peso_gelo,
                temperaturas['media'],
                umidade,
                self.sol_direto.get()
            )
            tempo_formatado = self.formatar_tempo(tempo_derretimento)

            # Verifica se tem logo
            logo_html = f'<img src="{self.logo_path}" class="logo" alt="GELO+">' if self.logo_path else ""

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        color: #333;
                    }}
                    .cabecalho {{
                        text-align: center;
                        margin-bottom: 30px;
                        border-bottom: 2px solid #0066cc;
                        padding-bottom: 20px;
                    }}
                    .logo {{
                        max-width: 150px;
                        margin-bottom: 15px;
                    }}
                    .titulo {{
                        color: #0066cc;
                        font-size: 24px;
                        margin: 10px 0;
                    }}
                    .data {{
                        color: #666;
                        font-size: 14px;
                    }}
                    .secao {{
                        margin: 20px 0;
                        padding: 15px;
                        background-color: #f8f9fa;
                        border-radius: 5px;
                    }}
                    .secao-titulo {{
                        color: #0066cc;
                        font-size: 18px;
                        margin-bottom: 10px;
                    }}
                    .info-linha {{
                        margin: 5px 0;
                        display: flex;
                        justify-content: space-between;
                    }}
                    .info-label {{
                        font-weight: bold;
                        color: #555;
                    }}
                    .destaque {{
                        background-color: #e6f3ff;
                        padding: 10px;
                        border-radius: 5px;
                        margin: 10px 0;
                    }}
                    .rodape {{
                        margin-top: 40px;
                        text-align: center;
                        font-size: 12px;
                        color: #666;
                        border-top: 1px solid #ddd;
                        padding-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="cabecalho">
                    {logo_html}
                    <h1 class="titulo">Relatório de Cálculo de Gelo</h1>
                    <div class="data">Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
                </div>

                <div class="secao">
                    <div class="secao-titulo">Informações do Pedido</div>
                    <div class="info-linha">
                        <span class="info-label">Volume solicitado:</span>
                        <span>{volume_solicitado:.1f}L</span>
                    </div>
                    <div class="info-linha">
                        <span class="info-label">Peso em gelo:</span>
                        <span>{peso_gelo:.1f}Kg</span>
                    </div>
                    <div class="info-linha">
                        <span class="info-label">Densidade do gelo:</span>
                        <span>{densidade:.3f}kg/L</span>
                    </div>
                </div>

                <div class="secao">
                    <div class="secao-titulo">Condições Ambientais</div>
                    <div class="info-linha">
                        <span class="info-label">Temperatura:</span>
                        <span>{temperaturas['min']:.1f}°C a {temperaturas['max']:.1f}°C (média: {temperaturas['media']:.1f}°C)</span>
                    </div>
                    <div class="info-linha">
                        <span class="info-label">Umidade do ar:</span>
                        <span>{self.umidade_min.get()}% a {self.umidade_max.get()}% (média: {umidade:.0f}%)</span>
                    </div>
                    <div class="info-linha">
                        <span class="info-label">Exposição solar:</span>
                        <span>{'Direta' if self.sol_direto.get() else 'Indireta'}</span>
                    </div>
                </div>

                <div class="secao">
                    <div class="secao-titulo">Quantidade de Sacos</div>
                    <div class="destaque">
                        <div class="info-linha">
                            <span class="info-label">Sacos de 10Kg:</span>
                            <span>{sacos_10kg} unidades</span>
                        </div>
                        <div class="info-linha">
                            <span class="info-label">Sacos de 3Kg:</span>
                            <span>{sacos_3kg} unidades</span>
                        </div>
                        <div class="info-linha">
                            <span class="info-label">Sacos de 1Kg:</span>
                            <span>{sacos_1kg} unidades</span>
                        </div>
                        <div class="info-linha" style="margin-top: 10px; border-top: 1px dashed #ccc; padding-top: 10px;">
                            <span class="info-label">Total em peso:</span>
                            <span>{peso_total_combinado:.1f}Kg</span>
                        </div>
                    </div>
                </div>

                <div class="secao">
                    <div class="secao-titulo">Tempo de Derretimento</div>
                    <div class="destaque">
                        <div class="info-linha">
                            <span class="info-label">Tempo estimado:</span>
                            <span>{tempo_formatado}</span>
                        </div>
                        <div class="info-linha">
                            <span class="info-label">Estado:</span>
                            <span>{self.get_descricao_temperatura(temperaturas['media'], self.sol_direto.get())}</span>
                        </div>
                    </div>
                </div>

                <div class="rodape">
                    GELO+ © {datetime.now().year} - Todos os direitos reservados<br>
                    Este documento é um relatório gerado automaticamente pelo sistema de cálculo GELO+
                </div>
            </body>
            </html>
            """
            return html
            
        except Exception as e:
            return f"<html><body><h1>Erro ao gerar relatório: {str(e)}</h1></body></html>"

    def imprimir(self):
        try:
            # Gera o HTML
            html_content = self.gerar_pagina_impressao()
            
            # Cria um arquivo temporário para o HTML
            temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'relatorio_temp.html')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Abre o arquivo no navegador padrão
            import webbrowser
            webbrowser.open(temp_file)
            
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraGelo(root)
    root.mainloop() 