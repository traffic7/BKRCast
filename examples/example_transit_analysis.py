"""
Example: Transit Network Analysis
분석 예제: 대중교통 네트워크 분석

This script demonstrates:
1. Analyzing transit boardings and alightings
2. Calculating route-level performance
3. Identifying top transit stops
4. Exporting transit results

이 스크립트는 다음을 시연합니다:
1. 대중교통 승하차 분석
2. 노선별 성능 계산
3. 주요 정류장 식별
4. 대중교통 결과 내보내기
"""

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

from EmmeProject import EmmeProject
import pandas as pd

def analyze_transit_network(project_path, tod='am'):
    """
    Analyze transit network performance
    
    Args:
        project_path: Path to Emme project (.emp file)
        tod: Time of day ('am', 'md', 'pm', 'ni')
    """
    
    print(f"=== Transit Network Analysis for {tod.upper()} ===\n")
    
    # 1. Initialize project
    print("1. Initializing Emme project...")
    project = EmmeProject(project_path)
    project.change_active_database(tod)
    
    # 2. Generate transit summary
    print("2. Generating transit summary...")
    df_line, df_node, df_segment = project.transit_summary()
    
    # 3. Route-level analysis
    print("\n3. Route Performance:")
    print("-" * 50)
    
    # Top routes by boardings
    top_routes = df_line.nlargest(10, 'boardings')[['route_code', 'description', 'boardings', 'time']]
    print("\n   Top 10 Routes by Boardings:")
    for idx, row in top_routes.iterrows():
        print(f"   {row['route_code']:>6}: {row['boardings']:>8.0f} boardings - {row['description']}")
    
    # 4. Stop-level analysis
    print("\n4. Stop Performance:")
    print("-" * 50)
    
    # Top stops by total boardings
    top_stops = df_node.nlargest(10, 'total_boarding')[['node_id', 'total_boarding', 'total_alighting']]
    print("\n   Top 10 Stops by Boardings:")
    for idx, row in top_stops.iterrows():
        print(f"   Stop {row['node_id']:>6}: {row['total_boarding']:>8.0f} boardings, {row['total_alighting']:>8.0f} alightings")
    
    # 5. Calculate transit metrics
    print("\n5. Transit Performance Metrics:")
    print("-" * 50)
    
    total_boardings = df_node['total_boarding'].sum()
    total_pmt = df_segment['PMT'].sum() if 'PMT' in df_segment.columns else 0
    
    print(f"   Total Boardings: {total_boardings:,.0f}")
    print(f"   Total PMT (Person-Miles-Traveled): {total_pmt:,.0f}")
    
    # Transfer analysis
    if 'transfer_boarding' in df_node.columns:
        total_transfers = df_node['transfer_boarding'].sum()
        transfer_rate = total_transfers / total_boardings * 100 if total_boardings > 0 else 0
        print(f"   Total Transfers: {total_transfers:,.0f}")
        print(f"   Transfer Rate: {transfer_rate:.1f}%")
    
    # 6. Segment analysis
    print("\n6. High-Volume Transit Segments:")
    print("-" * 50)
    
    if 'segment_volume' in df_segment.columns:
        high_vol_segments = df_segment.nlargest(10, 'segment_volume')[
            ['i_node', 'j_node', 'line_id', 'segment_volume']
        ]
        for idx, row in high_vol_segments.iterrows():
            print(f"   Line {row['line_id']:>6}, {row['i_node']:>6} → {row['j_node']:<6}: {row['segment_volume']:>6.0f} passengers")
    
    # 7. Export results
    print("\n7. Exporting results...")
    output_dir = 'outputs/examples'
    os.makedirs(output_dir, exist_ok=True)
    
    df_line.to_csv(f'{output_dir}/transit_routes_{tod}.csv', index=False)
    df_node.to_csv(f'{output_dir}/transit_stops_{tod}.csv', index=False)
    df_segment.to_csv(f'{output_dir}/transit_segments_{tod}.csv', index=False)
    
    print(f"   Saved route data to: {output_dir}/transit_routes_{tod}.csv")
    print(f"   Saved stop data to: {output_dir}/transit_stops_{tod}.csv")
    print(f"   Saved segment data to: {output_dir}/transit_segments_{tod}.csv")
    
    print("\n=== Analysis Complete ===")
    
    return df_line, df_node, df_segment

def analyze_daily_transit(project_path):
    """
    Analyze transit performance across all time periods
    
    Args:
        project_path: Path to Emme project (.emp file)
    """
    
    print("=== Daily Transit Analysis ===\n")
    
    all_lines = []
    all_nodes = []
    all_segments = []
    
    for tod in ['am', 'md', 'pm', 'ni']:
        print(f"Processing {tod.upper()}...")
        project = EmmeProject(project_path)
        project.change_active_database(tod)
        
        df_line, df_node, df_segment = project.transit_summary()
        
        all_lines.append(df_line)
        all_nodes.append(df_node)
        all_segments.append(df_segment)
    
    # Combine all periods
    df_daily_lines = pd.concat(all_lines, ignore_index=True)
    df_daily_nodes = pd.concat(all_nodes, ignore_index=True)
    df_daily_segments = pd.concat(all_segments, ignore_index=True)
    
    # Daily aggregation
    print("\n=== Daily Summary ===")
    print("-" * 50)
    
    # Daily boardings by route
    daily_route_boardings = df_daily_lines.groupby('route_code')['boardings'].sum()
    top_daily_routes = daily_route_boardings.nlargest(10)
    
    print("\nTop 10 Routes by Daily Boardings:")
    for route, boardings in top_daily_routes.items():
        print(f"   Route {route:>6}: {boardings:>10,.0f} daily boardings")
    
    # Daily boardings by stop
    daily_stop_boardings = df_daily_nodes.groupby('node_id')['total_boarding'].sum()
    top_daily_stops = daily_stop_boardings.nlargest(10)
    
    print("\nTop 10 Stops by Daily Boardings:")
    for stop, boardings in top_daily_stops.items():
        print(f"   Stop {stop:>6}: {boardings:>10,.0f} daily boardings")
    
    # Export daily summaries
    output_dir = 'outputs/examples'
    daily_route_boardings.to_csv(f'{output_dir}/daily_route_boardings.csv')
    daily_stop_boardings.to_csv(f'{output_dir}/daily_stop_boardings.csv')
    
    print(f"\nExported daily summaries to: {output_dir}/")
    print("\n=== Daily Analysis Complete ===")
    
    return df_daily_lines, df_daily_nodes, df_daily_segments

if __name__ == '__main__':
    # Example usage
    project_path = 'projects/LoadTripTables/LoadTripTables.emp'
    
    # Analyze single time period
    df_line, df_node, df_segment = analyze_transit_network(project_path, 'am')
    
    # Optional: Analyze all time periods and create daily summary
    # df_daily_lines, df_daily_nodes, df_daily_segments = analyze_daily_transit(project_path)
