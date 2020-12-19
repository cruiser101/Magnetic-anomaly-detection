function [ Za ] = magneticLPA( x, Deep, ra )
%UNTITLED 此处显示有关此函数的摘要
G=6.672*10^(-11);
u0=4*pi*10^(-7);
T=0.25*10^(-4);
JI=55*pi/180;
JD=-6.3*pi/180;
% JI=45*pi/180;
% JD=45*pi/180;
k=200;
M=k*T/u0;
S=pi*((ra+0.005)^2-ra^2);
%Deep=0.8;
sigema=7850-2600;
SiI =sin(JI);
CoI = cos(JI);
SiA = sin(JD);
CoA = cos(JD);

%第二步，给出表达式
Mcj=S*M*(((CoI^2)*(CoA^2)+SiI^2)^(1/2));
SiIS=SiI/(((CoI^2)*(CoA^2)+SiI^2)^(1/2));
CoIS=CoI*SiA/(((CoI^2)*(CoA^2)+SiI^2)^(1/2));
fenzi = u0*Mcj*10^9;
fenmu = 2*pi*((x^2 + Deep^2)^2);
Hax = -((Deep^2-x^2)*CoIS + 2*Deep*x*SiIS)*fenzi/fenmu;
Za = ((Deep^2-x^2)*SiIS - 2*Deep*x*CoIS)*fenzi/fenmu;
COJ = CoIS*CoI + SiIS*SiI;
SIJ = SiIS*CoI + CoIS*SiI;
detaT =  -((Deep^2-x^2)*COJ + 2*Deep*x*SIJ)*SiI*fenzi/(fenmu*SiIS);
end

