import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# --- Parâmetros da Simulação ---
# Você pode alterar estes valores para ver diferentes comportamentos

# Velocidades angulares (rad/s)
omega_rot = 0.2   # Velocidade de rotação (spin)
omega_p = 2.0    # Velocidade de precessão
omega_n = 15.0   # Velocidade de nutação

# Ângulos e Amplitudes (radianos)
theta_0 = np.pi / 6  # Ângulo médio de inclinação (precessão)
A_n = np.pi / 40   # Amplitude da nutação (quão forte é o "tremor")

# Geometria do Cone (corpo giratório)
cone_height = 4.0
cone_radius = 1.0
cone_points = 50

# Configurações da animação
dt = 0.02  # Passo de tempo
trail_length = 200 # Comprimento do rastro da ponta

# --- Configuração Inicial da Figura e Eixos ---
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
fig.subplots_adjust(left=0.1, bottom=0.25) # Ajusta espaço para os sliders

# --- Criação dos Vértices do Cone ---
# Cria a base circular do cone
theta_cone = np.linspace(0, 2 * np.pi, cone_points)
x_base = cone_radius * np.cos(theta_cone)
y_base = cone_radius * np.sin(theta_cone)
z_base = np.zeros(cone_points)

# Vértice do topo do cone
x_apex = np.array([0.])
y_apex = np.array([0.])
z_apex = np.array([cone_height])

# Combina os pontos para formar o cone (base e linhas até o topo)
# O cone é criado ao longo do eixo z do seu próprio sistema de coordenadas
cone_vertices = np.vstack([
    np.concatenate([x_base, x_apex]),
    np.concatenate([y_base, y_apex]),
    np.concatenate([z_base, z_apex])
])

# --- Funções para Matrizes de Rotação (Ângulos de Euler) ---
def rotation_matrix_z(angle):
    """Matriz de rotação em torno do eixo Z."""
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0,              0,             1]
    ])

def rotation_matrix_x(angle):
    """Matriz de rotação em torno do eixo X."""
    return np.array([
        [1, 0,              0            ],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle),  np.cos(angle)]
    ])

# --- Inicialização da Animação ---
# Desenha o cone na sua posição inicial
cone_plot = ax.plot_trisurf(cone_vertices[0, :], cone_vertices[1, :], cone_vertices[2, :], color='cyan', alpha=0.8)
# Linha para o rastro da ponta do cone
trail, = ax.plot([], [], [], 'r-', lw=1.5, label='Rastro da Ponta')
# Vetor para o eixo de rotação
axis_line, = ax.plot([], [], [], 'k-', lw=2, label='Eixo de Rotação')
# NOVO: Linha para o rastro de um ponto na base do cone
base_trail, = ax.plot([], [], [], 'b-', lw=1.5, label='Rastro da Base')

# Lista para armazenar as posições do rastro da ponta
trail_data = np.empty((3, trail_length))
trail_data[:] = np.nan
# NOVO: Lista para armazenar as posições do rastro da base
base_trail_data = np.empty((3, trail_length))
base_trail_data[:] = np.nan

def init():
    """Função de inicialização para a animação."""
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([0, 5])
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Simulação de Rotação, Precessão e Nutação')
    ax.grid(True)
    ax.legend()
    # Retorna os artistas que serão atualizados
    return cone_plot, trail, axis_line, base_trail

# --- Função de Animação (chamada a cada frame) ---
def animate(frame):
    global cone_plot, trail_data, base_trail_data # Permite modificar o plot do cone e os dados do rastro

    t = frame * dt

    # 1. Calcula os ângulos de Euler para o instante t
    phi = omega_p * t  # Precessão (rotação em torno do eixo Z global)
    theta = theta_0 + A_n * np.cos(omega_n * t) # Nutação (oscilação da inclinação)
    psi = omega_rot * t # Rotação (spin em torno do eixo z do cone)

    # 2. Constrói a matriz de rotação total (convenção Z-X'-Z'')
    Rz_phi = rotation_matrix_z(phi)
    Rx_theta = rotation_matrix_x(theta)
    Rz_psi = rotation_matrix_z(psi)
    
    # A rotação total transforma as coordenadas do corpo para as coordenadas do espaço
    R_total = Rz_phi @ Rx_theta @ Rz_psi

    # 3. Aplica a rotação aos vértices originais do cone
    rotated_vertices = R_total @ cone_vertices

    # 4. Atualiza o rastro da ponta do cone
    apex_position = rotated_vertices[:, -1]
    trail_data = np.roll(trail_data, -1, axis=1)
    trail_data[:, -1] = apex_position
    trail.set_data(trail_data[0, :], trail_data[1, :])
    trail.set_3d_properties(trail_data[2, :])

    # 5. NOVO: Atualiza o rastro do ponto na base
    base_point_position = rotated_vertices[:, 0] # Pega o primeiro ponto da base
    base_trail_data = np.roll(base_trail_data, -1, axis=1)
    base_trail_data[:, -1] = base_point_position
    base_trail.set_data(base_trail_data[0, :], base_trail_data[1, :])
    base_trail.set_3d_properties(base_trail_data[2, :])

    # 6. Atualiza o eixo de rotação
    origin = np.array([0, 0, 0])
    axis_end = apex_position
    axis_line.set_data([origin[0], axis_end[0]], [origin[1], axis_end[1]])
    axis_line.set_3d_properties([origin[2], axis_end[2]])

    # 7. Remove o cone antigo e desenha o novo
    cone_plot.remove()
    cone_plot = ax.plot_trisurf(
        rotated_vertices[0, :], rotated_vertices[1, :], rotated_vertices[2, :],
        color='cyan', alpha=0.8
    )

    return cone_plot, trail, axis_line, base_trail

# --- Sliders para controle interativo ---
ax_slider_rot = fig.add_axes([0.25, 0.15, 0.65, 0.03])
slider_rot = Slider(ax_slider_rot, 'Vel. Rotação', 0.0, 100.0, valinit=omega_rot)

ax_slider_prec = fig.add_axes([0.25, 0.1, 0.65, 0.03])
slider_prec = Slider(ax_slider_prec, 'Vel. Precessão', 0.0, 10.0, valinit=omega_p)

ax_slider_nut = fig.add_axes([0.25, 0.05, 0.65, 0.03])
slider_nut = Slider(ax_slider_nut, 'Vel. Nutação', 0.0, 50.0, valinit=omega_n)

# ESTA FUNÇÃO TAMBÉM FOI CORRIGIDA (REMOVIDO O RECUO)
def update_sliders(val):
    """Função para atualizar as variáveis globais quando um slider é movido."""
    global omega_rot, omega_p, omega_n
    omega_rot = slider_rot.val
    omega_p = slider_prec.val
    omega_n = slider_nut.val
    # Reseta os rastros para evitar saltos
    trail_data[:] = np.nan
    base_trail_data[:] = np.nan

slider_rot.on_changed(update_sliders)
slider_prec.on_changed(update_sliders)
slider_nut.on_changed(update_sliders)

# --- Cria e Inicia a Animação ---
ani = FuncAnimation(fig, animate, frames=800, init_func=init, interval=dt*1000, blit=False)

plt.show()
