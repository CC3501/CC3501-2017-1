%ver dominio en imagen adjunta

delta = 1;
n = 10/delta + 1; %nro de puntos en matriz final a modelar
mmodel = zeros(n, n);

subn = 5/delta; %subcuadrado

M = 75; %nro de incognitas (ver discretizacion de dominio)

A = zeros( M ); %matriz de incognitas
B = zeros ( M, 1 ); %vector soluciones

%ojo matrices: (linea, columna)

%condiciones de borde:
%borde superior y lateral izq dirichlet = 10
%extremos inf e izq, neumann = 0
%bordes internos neumann 2 hacia afuera (-2)

for i = linspace (1, 25, 25)
    
    if i > 5 && mod(i,5) ~= 0 && mod(i, 5) ~= 1
        %puntos internos, que tienen cuatro puntos validos alrededor
        %ecuacion tipica
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i-1) = 1;
        A(i,i+5) = 1;
        A(i,i-5) = 1;
    end
    
    if  i > 1 && i < 5
        %borde neumann inferior, sin esquinas
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i-1) = 1;
        A(i,i+5) = 2;
    end
    
    if i > 5 && mod(i, 5) == 1
        %puntos incognitos de la izquierda,
        %es decir, los que a su izq tienen el borde
        %dirichlet = 10
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i+5) = 1;
        A(i,i-5) = 1;
        
        B(i) = -10;
    end
    
    if i > 5 && mod(i, 5) == 0
        %borde derecho, neumann = 2 m/s
        A(i,i) = -4;
        A(i,i-1) = 2;
        A(i,i-5) = 1;
        A(i,i+5) = 1;
        
        B(i) = 2*delta*2;
    end
    
     if i == 1
        %caso especial, punto 1
        A(i,i) = -4;
        A(i,i+5) = 2;
        A(i,i+1) = 1;
        
        B(i) = -10;
     end
    
     
     if i == 5
         %esquina inferior derecha
        A(i,i) = -4;
        A(i,i-1) = 2;
        A(i,i+5) = 2;
        
        B(i) = 2 * delta * 2;
     end
     
     
end

for i = linspace (26, 75, 50)
    
    if i > 35 && mod(i, 10)~= 6 && mod(i, 10) ~= 5 && i < 66
        %puntos internos, que tienen cuatro puntos validos alrededor
        %ecuacion tipica
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i-1) = 1;
        A(i,i+10) = 1;
        A(i,i-10) = 1;
    end
    
    if i > 26 && i <= 30 
        %casos especiales, puntos en el borde
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i-1) = 1;
        A(i,i+10) = 1;
        A(i,i-5) = 1;
    end
    
    if i > 35 && mod(i, 10) == 5 && i ~= 75
        %borde derecho, neumann = 0 m/s
        A(i,i) = -4;
        A(i,i-1) = 2;
        A(i,i-10) = 1;
        A(i,i+10) = 1;
    end
    
    if i > 30 && i < 35
        %borde inferior, neumann = 2 m/s
        A(i,i) = -4;
        A(i,i-1) = 1;
        A(i,i+1) = 1;
        A(i,i+10) = 2;
        
        B(i) = 2*delta*2;
    end
    
    if i > 66 && i < 75
        %puntos incognitos de arriba,
        %es decir, los que arriba tienen el borde
        %dirichlet = 10
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i-10) = 1;
        A(i,i-1) = 1;
        
        B(i) = -10;
    end
    
    if i > 35 && mod(i, 10) == 6 && i ~= 66
        %puntos incognitos de la izquierda,
        %es decir, los que a su izq tienen el borde
        %dirichlet = 10
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i+10) = 1;
        A(i,i-10) = 1;
        
        B(i) = -10;
    end
    
    %puntos especiales (esquinas, etc)
    if i == 26
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i+10) = 1;
        A(i,i-5) = 1;
        
        B(i) = -10;
    end 
    
    if i == 66
        A(i,i) = -4;
        A(i,i+1) = 1;
        A(i,i-10) = 1;
        
        B(i) = -20;
    end
    
    if i == 75
        A(i,i) = -4;
        A(i,i-1) = 2;
        A(i,i-10) = 1;
        
        B(i) = -10;
    end
    
    if i == 35
        A(i,i) = -4;
        A(i,i-1) = 2;
        A(i,i+10) = 2;
       
        B(i) = 2*delta*2;
    end
    
end

X = linsolve(A,B) %X es nuestra matriz de incognitas (la cual, luego de
%resolver el sistema A*X = B contendrá el valor de cada uno de los puntos

%pasamos el vector X a la matriz de modelaje mmodel
p = 1;
for i = linspace(1, n, n)
    for j = linspace ( 1, n, n)
        if i < n && j > 1  
            if i < 6
                if j <= 6
                    mmodel(i,j) = X(p);
                    p = p + 1;
                else
                    mmodel(i,j) = NaN;
                end
            else
                mmodel(i,j) = X(p);
                p = p + 1;
            end
        end
    end
end
 
mmodel(n,:) = 10;
mmodel(:,1) = 10;

%mmodel = flipud(mmodel)

[dx, dy] = gradient(mmodel, delta);

V = zeros(n, n);

for i = linspace(1, n, n)
    for j = linspace ( 1, n, n)
        V(i,j) = sqrt(dx(i,j)^2 + dy(i,j)^2);
    end
end


lado = 0:delta:10;
[col, row] = meshgrid(lado,lado);

hold on 
%surf(mmodel)
%surf(V)
quiver(col, row, -1 * dx, -1 * dy); %flechas de velocidad
contour(col, row, mmodel, 20);
colormap(cool);
colorbar;
hold off

