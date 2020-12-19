function [ Hax, Hay, Za, detaT ] = magnetic( x, y )
%UNTITLED 此处显示有关此函数的摘要
G=6.672*10^(-11);
u0=4*pi*10^(-7);
T=0.525*10^(-4);
JI=55*pi/180;
JD=-6.3*pi/180;
% JI=45*pi/180;
% JD=45*pi/180;
k=200;
M=k*T/u0;
r=0.05;
Deep=0.9;
v=(4*pi*r^3)/3;
sigema=7850-2600;
Dis = x^2 + y^2 + Deep^2;
SiI =sin(JI);
CoI = cos(JI);
SiA = sin(JD);
CoA = cos(JD);


%第二步，给出表达式
Mcj=M*v;
fenzi = u0*Mcj*10^9;
fenmu = 4*pi*(x^2 + y^2 + Deep^2)^(5/2);
Hax = ((2*x^2-y^2-Deep^2)*CoI*CoA-3*Deep*x*SiI+3*x*y*CoI*SiA)*fenzi/fenmu;
Hay = ((2*y^2-x^2-Deep^2)*CoI*SiA-3*Deep*y*SiI+3*x*y*CoI*CoA)*fenzi/fenmu;
Za = ((2*Deep^2-x^2-y^2)*SiI-3*Deep*x*CoI*CoA-3*Deep*y*CoI*SiA)*fenzi/fenmu;
detaT = ((2*Deep^2-x^2-y^2)*SiI^2+(2*x^2-y^2-Deep^2)*(CoI^2)*(CoA^2) ...
    +(2*y^2-x^2-Deep^2)*(CoI^2)*(SiA^2)-3*x*Deep*2*SiI*CoI*CoA ...
    +3*x*y*(CoI^2)*2*SiA*CoA-3*y*Deep*2*SiI*CoI*SiA)*fenzi/fenmu;
%return Hax, Hay, Za;
end

