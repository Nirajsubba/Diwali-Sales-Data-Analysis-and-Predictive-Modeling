import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from io import StringIO

# Configure page
st.set_page_config(
    page_title="Diwali Sales Dashboard", 
    layout="wide",
    page_icon="🪔"
)

@st.cache_data
def load_data():
    # Sample data in case file loading fails
    sample_data = StringIO("""User_ID,Gender,Age,Age Group,Marital_Status,State,Zone,Occupation,Product_Category,Orders,Amount
1001,M,23,18-25,0,Haryana,Central,Healthcare,Clothing & Apparel,5,15000
1002,F,34,26-35,1,Karnataka,South,Engineer,Electronics,3,45000
1003,M,45,36-45,1,Maharashtra,West,Executive,Food,7,12000""")
    
    try:
        dt = pd.read_csv('Diwali Sales Data.csv', encoding='ISO-8859-1')
    except FileNotFoundError:
        st.warning("Using sample data as 'Diwali Sales Data.csv' not found")
        dt = pd.read_csv(sample_data)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()
    
    # Clean data
    dt = dt.drop(columns=['Status', 'unnamed1'], errors='ignore')
    
    # Validate critical columns
    required_cols = ['Amount', 'Orders', 'User_ID', 'Gender', 'Age Group', 'Zone', 'Product_Category']
    missing = [col for col in required_cols if col not in dt.columns]
    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()
    
    # Handle missing values
    if dt['Amount'].isna().any():
        dt['Amount'] = dt['Amount'].fillna(dt['Amount'].median())
    
    return dt

dt = load_data()

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 14px;
        color: #6c757d;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #212529;
    }
    .stMultiSelect [data-baseweb=tag] {
        background-color: #4e79a7;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

def update_filters():
    st.session_state.filters_updated = True

with st.sidebar:
    gender_filter = st.multiselect(
        "Select Gender",
        options=dt['Gender'].unique(),
        default=dt['Gender'].unique(),
        key='gender_filter',
        on_change=update_filters
    )
    
    age_filter = st.multiselect(
        "Select Age Group",
        options=sorted(dt['Age Group'].unique()),
        default=sorted(dt['Age Group'].unique()),
        key='age_filter',
        on_change=update_filters
    )
    
    zone_filter = st.multiselect(
        "Select Zone",
        options=dt['Zone'].unique(),
        default=dt['Zone'].unique(),
        key='zone_filter',
        on_change=update_filters
    )
    
    product_filter = st.multiselect(
        "Select Product Category",
        options=dt['Product_Category'].unique(),
        default=dt['Product_Category'].unique(),
        key='product_filter',
        on_change=update_filters
    )
    
    # Download filtered data
    st.download_button(
        label="📥 Download Filtered Data",
        data=dt[
            (dt['Gender'].isin(gender_filter)) &
            (dt['Age Group'].isin(age_filter)) &
            (dt['Zone'].isin(zone_filter)) &
            (dt['Product_Category'].isin(product_filter))
        ].to_csv(index=False).encode('utf-8'),
        file_name='filtered_diwali_sales.csv',
        mime='text/csv'
    )

# Apply filters
filtered_dt = dt[
    (dt['Gender'].isin(gender_filter)) &
    (dt['Age Group'].isin(age_filter)) &
    (dt['Zone'].isin(zone_filter)) &
    (dt['Product_Category'].isin(product_filter))
]

# Title and description
st.title("🪔 Diwali Sales Dashboard")
st.markdown("Explore sales performance during the Diwali festival season. Use the filters in the sidebar to analyze different segments.")

# KPI cards
total_sales = filtered_dt['Amount'].sum()
total_orders = filtered_dt['Orders'].sum()
avg_order_value = total_sales / total_orders if total_orders > 0 else 0
unique_customers = filtered_dt['User_ID'].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown('<div class="metric-container"><div class="metric-label">Total Sales Amount</div><div class="metric-value">₹{:,.0f}</div></div>'.format(total_sales), unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="metric-container"><div class="metric-label">Total Orders</div><div class="metric-value">{:,}</div></div>'.format(total_orders), unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="metric-container"><div class="metric-label">Avg Order Value</div><div class="metric-value">₹{:,.2f}</div></div>'.format(avg_order_value), unsafe_allow_html=True)
with kpi4:
    st.markdown('<div class="metric-container"><div class="metric-label">Unique Customers</div><div class="metric-value">{:,}</div></div>'.format(unique_customers), unsafe_allow_html=True)

# Visualization functions
def plot_gender_pie(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    colors = ['#4e79a7', '#f28e2b']  # Blue and orange
    wedges, texts, autotexts = ax.pie(
        data, 
        labels=data.index,
        autopct=lambda pct: f'{pct:.1f}%',
        startangle=90,
        colors=colors,
        textprops={'color': 'white', 'weight': 'bold'}
    )
    ax.axis('equal')
    ax.set_title("Sales Distribution by Gender", pad=20)
    plt.setp(autotexts, size=10, weight="bold")
    return fig

def plot_horizontal_bar(data, x_col, y_col, title, top_n=10):
    # Get top N items
    top_data = data.sort_values(x_col, ascending=False).head(top_n)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Create horizontal bar plot with category names
    bars = ax.barh(
        top_data[y_col],
        top_data[x_col],
        color=sns.color_palette("viridis", len(top_data))
    )
    
    # Add value labels
    ax.bar_label(bars, fmt='%.0f', padding=3, fontsize=10)
    
    # Customize appearance
    ax.set_title(title, pad=15)
    ax.set_xlabel('Total Amount' if x_col == 'Amount' else 'Number of Orders')
    ax.set_ylabel(y_col.replace('_', ' ').title())
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    
    # Adjust layout for long category names
    plt.rcParams['ytick.labelsize'] = 10
    fig.subplots_adjust(left=0.3)
    
    return fig

def plot_vertical_bar(data, x_col, y_col, title, order=None, rotation=45):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    if order is not None:
        data[x_col] = pd.Categorical(data[x_col], categories=order, ordered=True)
        data = data.sort_values(x_col)
    
    bars = ax.bar(
        data[x_col],
        data[y_col],
        color=sns.color_palette("husl", len(data))
    )
    
    # Add value labels on top of bars
    ax.bar_label(bars, fmt='%.0f', padding=0, fontsize=10)
    
    ax.set_title(title, pad=15)
    ax.set_ylabel('Total Amount')
    ax.set_xlabel(x_col.replace('_', ' ').title())
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    
    return fig

# Precompute data for visualizations
@st.cache_data
def prepare_visualization_data(_filtered_dt):
    gender_sales = _filtered_dt.groupby('Gender')['Amount'].sum()
    age_sales = _filtered_dt.groupby('Age Group')['Amount'].sum().reset_index()
    zone_sales = _filtered_dt.groupby('Zone')['Amount'].sum().reset_index()
    
    product_sales = _filtered_dt.groupby('Product_Category')['Amount'].sum().reset_index()
    product_orders = _filtered_dt.groupby('Product_Category')['Orders'].sum().reset_index()
    
    combo = _filtered_dt.groupby(['Age Group', 'Gender'])['Amount'].sum().reset_index()
    
    return {
        'gender_sales': gender_sales,
        'age_sales': age_sales,
        'zone_sales': zone_sales,
        'product_sales': product_sales,
        'product_orders': product_orders,
        'combo': combo
    }

viz_data = prepare_visualization_data(filtered_dt)

# First row of charts
col1, col2, col3 = st.columns(3)

with col1:
    try:
        st.pyplot(plot_gender_pie(viz_data['gender_sales']))
    except Exception as e:
        st.error(f"Error displaying gender distribution: {str(e)}")

with col2:
    try:
        age_order = ['0-17','18-25','26-35','36-45','46-50','51-55','55+']
        st.pyplot(plot_vertical_bar(
            viz_data['age_sales'],
            x_col='Age Group',
            y_col='Amount',
            title='Total Sales by Age Group',
            order=age_order,
            rotation=30
        ))
    except Exception as e:
        st.error(f"Error displaying age group sales: {str(e)}")

with col3:
    try:
        st.pyplot(plot_vertical_bar(
            viz_data['zone_sales'],
            x_col='Zone',
            y_col='Amount',
            title='Sales by Zone',
            rotation=30
        ))
    except Exception as e:
        st.error(f"Error displaying zone sales: {str(e)}")

# Second row of charts
col1, col2, col3 = st.columns(3)

with col1:
    try:
        st.pyplot(plot_horizontal_bar(
            viz_data['product_sales'],
            x_col='Amount',
            y_col='Product_Category',
            title='Sales by Product Category'
        ))
    except Exception as e:
        st.error(f"Error displaying product sales: {str(e)}")

with col2:
    try:
        st.pyplot(plot_horizontal_bar(
            viz_data['product_orders'],
            x_col='Orders',
            y_col='Product_Category',
            title='Most Ordered Product Categories'
        ))
    except Exception as e:
        st.error(f"Error displaying product orders: {str(e)}")

with col3:
    try:
        fig, ax = plt.subplots(figsize=(8, 5))
        age_order = ['0-17','18-25','26-35','36-45','46-50','51-55','55+']
        sns.barplot(
            data=viz_data['combo'], 
            x='Age Group', 
            y='Amount', 
            hue='Gender',
            order=age_order,
            ax=ax,
            palette=['#4e79a7', '#f28e2b']
        )
        ax.set_title('Sales by Age Group and Gender', pad=15)
        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        plt.xticks(rotation=30)
        plt.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error displaying age-gender combo: {str(e)}")

# Add expandable raw data view
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered_dt, height=200)

# Add footer
st.markdown("---")
current_date = pd.Timestamp.now().strftime("%Y-%m-%d")
st.markdown(f"""
<div style="font-size:12px; color:#6c757d; text-align:center; padding:10px;">
    Dashboard created with ❤️ using Streamlit | Data last updated: {current_date}
</div>
""", unsafe_allow_html=True)