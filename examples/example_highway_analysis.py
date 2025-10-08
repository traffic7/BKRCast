"""
Example: Highway Network Analysis
분석 예제: 도로 네트워크 분석

This script demonstrates:
1. Loading a BKRCast Emme project
2. Calculating traffic performance metrics
3. Identifying congested links
4. Exporting results to CSV

이 스크립트는 다음을 시연합니다:
1. BKRCast Emme 프로젝트 로드
2. 교통 성능지표 계산
3. 혼잡 링크 식별
4. 결과를 CSV로 내보내기
"""

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

from EmmeProject import EmmeProject
import pandas as pd

def analyze_highway_network(project_path, tod='am'):
    """
    Analyze highway network performance
    
    Args:
        project_path: Path to Emme project (.emp file)
        tod: Time of day ('am', 'md', 'pm', 'ni')
    """
    
    print(f"=== Highway Network Analysis for {tod.upper()} ===\n")
    
    # 1. Initialize project
    print("1. Initializing Emme project...")
    project = EmmeProject(project_path)
    project.change_active_database(tod)
    
    # 2. Calculate V/C ratio if not already calculated
    print("2. Calculating V/C ratio...")
    try:
        project.network_calculator(
            "link_calculation",
            result='@vc_ratio',
            expression='@tveh / ul2'
        )
    except:
        print("   V/C ratio already exists or calculation failed")
    
    # 3. Get network and extract data
    print("3. Extracting network data...")
    network = project.current_scenario.get_network()
    
    link_data = []
    for link in network.links():
        link_data.append({
            'i_node': link.i_node.id,
            'j_node': link.j_node.id,
            'length': link.length,
            'capacity': link['ul2'] if 'ul2' in dir(link) else 0,
            'volume': link['@tveh'],
            'vc_ratio': link['@vc_ratio'] if '@vc_ratio' in link.get_extra_attributes() else 0,
            'func_class': link['@class'] if '@class' in link.get_extra_attributes() else 0
        })
    
    df = pd.DataFrame(link_data)
    
    # 4. Calculate performance metrics
    print("\n4. Performance Metrics:")
    print("-" * 50)
    
    # VMT (Vehicle-Miles-Traveled)
    vmt = (df['volume'] * df['length']).sum()
    print(f"   Total VMT: {vmt:,.0f} vehicle-miles")
    
    # Identify congestion levels
    df['congestion_level'] = pd.cut(df['vc_ratio'], 
                                      bins=[0, 0.8, 1.0, 1.2, float('inf')],
                                      labels=['Low', 'Moderate', 'High', 'Severe'])
    
    congestion_summary = df.groupby('congestion_level').agg({
        'length': 'sum',
        'volume': 'sum'
    }).round(2)
    
    print("\n   Congestion Summary:")
    print(congestion_summary)
    
    # 5. Identify top congested links
    print("\n5. Top 10 Most Congested Links:")
    print("-" * 50)
    
    congested = df[df['vc_ratio'] > 1.0].sort_values('vc_ratio', ascending=False).head(10)
    for idx, row in congested.iterrows():
        print(f"   {row['i_node']:>6} → {row['j_node']:<6}: V/C = {row['vc_ratio']:.2f}")
    
    # 6. Export results
    print("\n6. Exporting results...")
    output_dir = 'outputs/examples'
    os.makedirs(output_dir, exist_ok=True)
    
    # All links
    df.to_csv(f'{output_dir}/highway_analysis_{tod}.csv', index=False)
    print(f"   Saved to: {output_dir}/highway_analysis_{tod}.csv")
    
    # Congested links only
    congested_all = df[df['vc_ratio'] > 1.0]
    congested_all.to_csv(f'{output_dir}/congested_links_{tod}.csv', index=False)
    print(f"   Saved to: {output_dir}/congested_links_{tod}.csv")
    
    print("\n=== Analysis Complete ===")
    
    return df

if __name__ == '__main__':
    # Example usage
    project_path = 'projects/LoadTripTables/LoadTripTables.emp'
    
    # Analyze AM period
    df_am = analyze_highway_network(project_path, 'am')
    
    # Optional: Analyze all time periods
    # for tod in ['am', 'md', 'pm', 'ni']:
    #     analyze_highway_network(project_path, tod)
