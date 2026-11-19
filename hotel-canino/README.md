# Titio Cachorrão — Hotel canino

Protótipo local em React + Python, com SQLite. Cadastro de cães e tutores; reserva de estadias; check-in e check-out com registro de hora; painel operacional; código único de coleira; simulação de leitura. Não há hardware conectado.

## Executar

Requer Python 3.10 ou superior. Não requer pip.

```powershell
python backend/server.py
```

Abra http://localhost:4180. O React está incluído nos arquivos locais. Fontes externas são opcionais; o navegador usa fontes do sistema se estiver offline. O backend atende apenas este computador. Os dados são persistidos em backend/hotel.db, criado automaticamente. Faça backup desse arquivo com o servidor parado.

## Uso

1. Em Cães e tutores, cadastre o cão, tutor, telefone e código da coleira.
2. Crie uma estadia com entrada e saída previstas (a saída deve ser posterior à entrada).
3. No painel, faça check-in na chegada e check-out na entrega ao tutor.
4. Em Identificação, simule uma leitura com o código cadastrado.

Os indicadores diários usam a data local do navegador. Os horários reais das transições ficam no banco. Datas previstas não são substituídas pelas datas reais. Reservas conflitantes do mesmo cão são recusadas. O aplicativo inicia sem dados fictícios.

## Limites desta versão

Sem autenticação, edição/exclusão, cobrança, capacidade máxima, múltiplas unidades ou conexão real com leitores. Adequado para demonstração local; antes de uso operacional, implementar autenticação, backup, permissões e integração validada. Uma leitura identifica o cão e registra um evento; ela não encerra uma estadia automaticamente.

Veja docs/AUTOMACAO.md para a proposta de automação.


## Relatórios e diárias

Acesse Relatórios e diárias. O valor inicial é R$ 110,00 por noite e pode ser alterado para novas reservas. Cada estadia mantém sua diária, inclusive após mudanças no cadastro do preço. Estadias anteriores a essa funcionalidade recebem a diária inicial de R$ 110,00.

O cálculo usa as noites reservadas (saída prevista menos entrada prevista), multiplicadas pela diária da reserva. Horários reais de check-in e check-out não recalculam esse período. Filtre por cão para ver o histórico, noites, diária e total. Valores previstos e estadias encerradas são apresentados separadamente. Não há registro de pagamentos, descontos ou saldo em aberto nesta versão.


## Dados do estabelecimento

Informações fornecidas pelo responsável por imagem:

- Titio Cachorrão.
- Slogan: Há mais de 30 anos cuidando do seu pet!
- R. Joaquim Bernardes Borges, 794 — Centro — Itu, São Paulo.
- Telefone: (11) 4024-0420.
- Instagram: @titiocachorrao.
- Facebook: facebook.com/titiocachorraopetshop.
