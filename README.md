Simulação 3D do Movimento de um Corpo Rígido
Este repositório contém o código-fonte em Python para a simulação e visualização 3D dos movimentos de um corpo rígido (rotor simétrico). O objetivo é fornecer uma ferramenta visual interativa para o estudo da precessão, nutação e rotação (spin), conceitos fundamentais da Mecânica Lagrangiana e dos Ângulos de Euler.
Este código foi desenvolvido como material suplementar para o relatório de Iniciação Científica "Introdução ao Cálculo de Variações e suas Aplicações à Mecânica Clássica", de autoria de João Victor Pinheiro Lacerda, sob orientação do Prof. Dr. Walter de Siqueira Pedra (ICMC/EESC - USP).
(Sugestão: Tire um screenshot da sua animação, faça o upload em um site como o Imgur e cole o link aqui para ter uma pré-visualização no seu README).
Pré-requisitos
Para executar esta simulação, você precisará ter o Python 3 instalado, juntamente com as seguintes bibliotecas
NumPy: Para cálculos numéricos.
Matplotlib: Para a criação dos gráficos e da animação.
Você pode instalar as dependências necessárias utilizando o pip:
    pip install numpy matplotlib
Como UsarClone este repositório para a sua máquina local:
    git clone https://github.com/seu-usuario/seu-repositorio.git
Navegue até o diretório do projeto:
    cd seu-repositorio
Execute o script Python:
    python nome_do_seu_script.py
Uma janela do Matplotlib será aberta, exibindo a animação 3D.
Controles Interativos.
A simulação possui sliders na parte inferior da janela que permitem alterar os seguintes parâmetros em tempo real:
Vel. Rotação: Altera a velocidade de spin (omega_rot) do corpo em torno do seu próprio eixo de simetria.
Vel. Precessão: Altera a velocidade (Omega_p) com que o eixo de simetria descreve um cone no espaço.
Vel. Nutação: Altera a frequência (omega_n) da oscilação (tremor) do eixo de simetria.
Parâmetros do Código.
Dentro do script, você pode modificar os seguintes parâmetros iniciais para explorar diferentes comportamentos dinâmicos:
omega_rot: Velocidade angular de rotação (spin) inicial.
omega_p: Velocidade angular de precessão inicial.
omega_n: Velocidade angular de nutação inicial.
theta_0: Ângulo médio de inclinação do eixo do corpo (ângulo de precessão).
A_n: Amplitude do movimento de nutação.
Citação.
Se você utilizar este código em seu trabalho, por favor, cite o repositório. Você pode usar o seguinte formato BibTeX:
    @misc{Lacerda2025Simulacao,
    author       = {Jo{\~a}o Victor Pinheiro Lacerda},
    title        = {Simula{\c c}{\~a}o 3D do Movimento de um Corpo R{\'i}gido},
    year         = {2025},
    publisher    = {GitHub},
    journal      = {GitHub repository},
    howpublished = {\url{https://github.com/seu-usuario/seu-repositorio}}
    }
Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
