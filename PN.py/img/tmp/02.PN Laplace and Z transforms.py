from PNlib.PolyNum import PolyNum

# Z-transform (live example):
h = 0.01 # sampling period
p = 1/h * PolyNum('const:(~2~,-4~4~-4~4~...~)')
# p_trap(h) = (2/h)*(~1~-1~) / (~1~1~) = (1/h) * (~2~,-4~4~-4~4~...~)
E_0 = 10  # const for t > 0
E = E_0 * 0.5 * PolyNum('const:(~1~,2~2~2~2~...~)')
R, L, C = 20, 2, 1e-3
Z_C = 1/(p*C)
Z = R + p*L + Z_C
U_C = E * Z_C / Z

# plt.plot(E, 'r--',U_C, 'b-') 
import matplotlib.pyplot as plt
plt.plot(E, 'r--',U_C, 'b-')
plt.text(0.6,10.4,"$ e(t) $", fontsize=16, color='red')
plt.text(21,12.2,"$ u_C(t) $", fontsize=16, color='blue')
plt.grid(b=True)
plt.show()

