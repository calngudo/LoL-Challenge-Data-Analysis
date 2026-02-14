import pandas as pd, seaborn as sns, matplotlib.pyplot as plt


#Heatmap of Win Rates by Champion and Position (Needs to be improved and look more comprehensive)
def heatmap_champions(df):
    pivot_table = df.pivot_table(index='champion_name', columns='team_position', values='win', aggfunc='mean')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, cmap='coolwarm', linewidths=.5)
    plt.title('Win Rate by Champion and Position')
    plt.xlabel('Team Position')
    plt.ylabel('Champion Name')
    plt.show()

#Player Role Distribution
def plot_roles(df):
    role_pct = df.groupby(['summoner_name', 'team_position']).size().unstack(fill_value=0)
    role_pct = role_pct.div(role_pct.sum(axis=1), axis=0) * 100
    
    role_pct.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.title('Player Role Distribution (%)')
    plt.xlabel('Player')
    plt.ylabel('Percentage (%)')
    plt.legend(title='Role')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#Winrate by Player and Role
def plot_winrate(df):
    winrate = df.groupby(['summoner_name', 'team_position'])['win'].mean() * 100
    winrate = winrate.unstack()
    
    winrate.plot(kind='bar', figsize=(12, 6))
    plt.title('Winrate by Player and Role (%)')
    plt.xlabel('Player')
    plt.ylabel('Winrate (%)')
    plt.legend(title='Role')
    plt.xticks(rotation=45)
    plt.axhline(50, color='red', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    #Top 5 Champions by Role
def plot_top_champs(df):
    roles = df['team_position'].unique()
    
    fig, axes = plt.subplots(1, len(roles), figsize=(18, 5))
    
    for i, role in enumerate(roles):
        top5 = df[df['team_position'] == role]['champion_name'].value_counts().head(5)
        top5.plot(kind='barh', ax=axes[i])
        axes[i].set_title(f'{role}')
        axes[i].invert_yaxis()
    
    plt.tight_layout()
    plt.show()