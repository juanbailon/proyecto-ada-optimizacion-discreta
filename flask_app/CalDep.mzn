% Parámetros
int: n;                          % Número de equipos
array[1..n, 1..n] of int: D;     % Matriz de distancias
int: Min;                        % Tamaño mínimo de giras y permanencias
int: Max;                        % Tamaño máximo de giras y permanencias

% Variables
array[1..2*(n-1), 1..n] of var -n..n: Cal;  % Calendario de partidos
array[1..2*(n-1), 1..n] of var 0..Max: Giras;
array[1..2*(n-1), 1..n] of var 0..Max: Permanencias;
var int: costoTotal;


% Restricciones

% Cal[i, j] toma valores en [-n, n]
% Restricción: Cal[i, j] ≠ j
constraint forall(i in 1..2*(n-1), j in 1..n) (
    abs(Cal[i, j]) <= n 
 /\ abs(Cal[i, j]) != j 
);

% Restricción: equipos no juegan dos veces en una misma fecha consecutivas 
constraint forall(i in 1..2*(n-1), j in 1..n-1) (
    abs(Cal[i, j]) != abs(Cal[i, j+1]) 
);

% Restricción: equipos no juegan el mismo partido en dos fechas consecutivas 
constraint forall(i in 1..2*(n-1)-1, j in 1..n) (
    abs(Cal[i, j]) != abs(Cal[i+1, j]) 
);

% Restricción: Cal[i, j] = k si y solo si Cal[i, k] = -j
constraint forall(i in 1..2*(n-1), j in 1..n) (
    let {var int: k = abs(Cal[i, j])} in
        (Cal[i, j] > 0 /\ Cal[i, k] = -j) \/ (Cal[i, j] < 0 /\ Cal[i, k] = j) 
);

% Restricción: para cada j, k ≠ j, existe i1, i2 diferentes tal que Cal[i1, j] = k y Cal[i2, j] = -k
constraint forall(j in 1..n, k in 1..n where k != j) (
    exists(i1 in 1..2*(n-1)) (
        Cal[i1, j] = k
    ) /\ exists(i2 in 1..2*(n-1)) (
        Cal[i2, j] = -k
    )
);


%No se permiten permanenecias menores a Min
%constraint forall(j in 1..n, i in 1..2*(n-1) )(

 % (i == 2*(n-1) /\ Cal[i,j] > 0 -> Permanencias[i,j] >= Min) \/
 % (i < 2*(n-1) /\ Cal[i,j] < 0 /\ Cal[i-1,j] > 0 -> Permanencias[i-1,j] >= Min)
  
%);

%No se permiten permanenecias menores a Min
constraint forall(j in 1..n, i in 1..2*(n-1))(
  if i == 2*(n-1) then 
    if Cal[i,j] > 0 then 
    Permanencias[i,j] >= Min
    else true
    endif
  else
    if Cal[i,j] < 0 then 
      if Cal[i-1,j] > 0 then 
      Permanencias[i-1,j] >= Min
      else true              
      endif
    else true               
    endif
  endif        
);%Las permanencias consecutivas no pueden ser menores que Min


%No se permiten permanencias mayores a Max
constraint forall(i in 1..2*(n-1), j in 1..n) (
  Permanencias[i, j] = (Cal[i, j] > 0) * (if i == 1 then 1 else Permanencias[i-1, j] + 1 endif)
);


%No se permiten giras menores a Min
%constraint forall(j in 1..n, i in 1..2*(n-1))(
%  (i == 2*(n-1) /\ Cal[i,j] < 0 -> Giras[i,j] >= Min) \/
%  (i < 2*(n-1) /\ Cal[i,j] > 0 /\ Cal[i-1,j] < 0 -> Giras[i-1,j] >= Min)
%);
%No se permiten giras menores a Min
constraint forall(j in 1..n, i in 1..2*(n-1))(
if i == 2*(n-1) then 
  if Cal[i,j] < 0 then 
  Giras[i,j]>=Min
  else true
  endif
else
  if (Cal[i,j] > 0)then 
    if(Cal[i-1,j] < 0)
    then Giras[i-1,j]>=Min  
    else true            
    endif   
  else true            
  endif
endif            
);%Las giras consecutivas no pueden ser menores que Min

%No se permiten giras mayores a Max
constraint forall(i in 1..2*(n-1), j in 1..n) (
  Giras[i, j] = (Cal[i, j] < 0) * (if i == 1 then 1 else Giras[i-1, j] + 1 endif)
);

constraint costoTotal = sum([
if i == 1 then 
  if Cal[i,j] < 0 then D[j, abs(Cal[i,j])]
  else 0
  endif
elseif i == 2*(n-1) then 
  if Cal[i-1,j] < 0 then 
    if Cal[i,j] > 0 then D[abs(Cal[i-1, j]), j]
    else  D[abs(Cal[i-1, j]), abs(Cal[i,j])] + D[abs(Cal[i,j]), j]
    endif
  else 
    if Cal[i,j] > 0 then 0
    else D[j, abs(Cal[i,j])] + D[abs(Cal[i,j]), j]
    endif    
  endif  
else 
  if Cal[i-1,j] < 0 then 
    if Cal[i,j] > 0 then D[abs(Cal[i-1, j]), j]
    else  D[abs(Cal[i-1, j]), abs(Cal[i,j])]
    endif
  else 
    if Cal[i,j] > 0 then 0
    else D[j, abs(Cal[i,j])]
    endif    
  endif    
endif
| j in 1..n, i in 1..2*(n-1) ]);

solve minimize costoTotal;

output["Costo: \(costoTotal) , Matriz: \(Cal)"]
