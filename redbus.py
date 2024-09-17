import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Set page configuration
st.set_page_config(layout="wide")

def set_background():
    """Set the background image for the Streamlit app."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/premium-vector/trip-booking-web-banner-landing-page-buying-ticket-bus_277904-15153.jpg?size=626&ext=jpg&ga=GA1.1.1814242882.1726069051&semt=ais_hybrid");
        background-size: cover;
        background-position: center;
    }
    </style>
    """, unsafe_allow_html=True)

def connect_mysql():
    """Establish a connection to the MySQL server using SQLAlchemy."""
    try:
        engine = create_engine("mysql+mysqlconnector://root:selva@localhost:3306/redbus_details")
        return engine
    except SQLAlchemyError as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def fetch_data_from_db(query=None):
    """Fetch data from the MySQL database using SQLAlchemy."""
    engine = connect_mysql()
    if engine:
        try:
            df = pd.read_sql(query, engine) if query else pd.read_sql("SELECT * FROM redbus_details", engine)
            return df
        except SQLAlchemyError as e:
            st.error(f"Error fetching data: {e}")
            return None
    return None

def find_closest_matches(df, selected_criteria):
    """Find the closest matches by relaxing some filters."""
    df['match_count'] = (
        (df['bus_type'] == selected_criteria['bus_type']).astype(int) +
        (df['price'].between(selected_criteria['min_price'], selected_criteria['max_price'])).astype(int) +
        (df['departing_time'] == selected_criteria['departing_time']).astype(int) +
        (df['reaching_time'] == selected_criteria['reaching_time']).astype(int) +
        (df['duration'] == selected_criteria['duration']).astype(int) +
        (df['star_rating'] == selected_criteria['star_rating']).astype(int)
    )
    df_sorted = df.sort_values(by='match_count', ascending=False)
    return df_sorted[df_sorted['match_count'] > 0]

def main():
    """Main function to run the Streamlit app."""
    
    # Set background for all pages
    set_background()

    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    # Sidebar menu
    st.sidebar.title(" Main Menu")
    if st.sidebar.button(" Home"):
        st.session_state.page = 'home'
    if st.sidebar.button(" Select the Bus"):
        st.session_state.page = 'bus_details'
    if st.sidebar.button(" Book a Bus"):
        st.session_state.page = 'booking'

    # Home Page
    if st.session_state.page == 'home':
        st.title(" Welcome to RedBus Details App!")
        
        # Content with background image
        st.image("data:image/png;base64,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")

        # Layout management: Split into two columns for better organization
        col1, col2 = st.columns([2, 1])  # Two-thirds for left column, one-third for right

        with col1:
            st.subheader("Why Use Our App? ")
            st.write(""" 
            - ** Find Buses:** Easily find bus routes and schedules.
            - ** Filter by Price:** Set your budget and find the best options.
            - ** High Ratings:** Choose only the top-rated buses for your journey.
            """)
        
        with col2:
            st.subheader("Quick Start")
            st.write("Press the button below to explore available buses:")
            # Add a large button for emphasis
            if st.button(" Get Started"):
                st.session_state.page = 'bus_details'

        # Add a footer with instructions and tips
        st.markdown("---")
        st.subheader("How It Works ")
        st.write("""
        1. **Select a Route:** Choose your desired route.
        2. **Filter by Preferences:** Filter buses by seat type, price, and ratings.
        3. **Book Your Bus:** Select a bus and complete the booking in a few easy steps!
        """)
        
        st.info("Ready to start? Use the button above or the menu on the left!")
    
    # Bus Details Page
    elif st.session_state.page == 'bus_details':
        bus_df = fetch_data_from_db()

        if bus_df is not None and not bus_df.empty:
            st.header(" Select Your Route")
            routes = bus_df['route_name'].unique().tolist()
            selected_route = st.selectbox(" Choose a Route", routes)

            route_filtered_df = bus_df[bus_df['route_name'] == selected_route]

            if not route_filtered_df.empty:
                st.markdown("### 🎫 Bus Options")
                col1, col2 = st.columns(2)
                with col1:
                    seat_types = route_filtered_df['bus_type'].unique().tolist()
                    selected_seat_type = st.selectbox(" Seat Type", seat_types)
                with col2:
                    min_price, max_price = int(route_filtered_df['price'].min()), int(route_filtered_df['price'].max())
                    selected_price_range = st.slider(" Price Range", min_price, max_price, (min_price, max_price))

                col3, col4 = st.columns(2)
                with col3:
                    available_durations = route_filtered_df['departing_time'].unique().tolist()
                    selected_duration = st.selectbox(" Departure Time", available_durations)
                with col4:
                    reaching_times = route_filtered_df['reaching_time'].unique().tolist()
                    selected_reaching_time = st.selectbox(" Reaching Time", reaching_times)

                duration_times = route_filtered_df['duration'].unique().tolist()
                selected_duration_time = st.selectbox(" Duration", duration_times)

                rating = route_filtered_df['star_rating'].unique().tolist()
                selected_operator = st.selectbox(" Bus Rating", rating)

                filtered_df = route_filtered_df[
                    (route_filtered_df['bus_type'] == selected_seat_type) &
                    (route_filtered_df['price'] >= selected_price_range[0]) &
                    (route_filtered_df['price'] <= selected_price_range[1]) &
                    (route_filtered_df['departing_time'] == selected_duration) &
                    (route_filtered_df['reaching_time'] == selected_reaching_time) &
                    (route_filtered_df['duration'] == selected_duration_time) &
                    (route_filtered_df['star_rating'] == selected_operator)
                ]

                if not filtered_df.empty:
                    st.header(" Select Your Bus")
                    bus_names = filtered_df['bus_name'].unique().tolist()
                    selected_bus_name = st.selectbox(" Available Buses", bus_names)

                    final_filtered_df = filtered_df[filtered_df['bus_name'] == selected_bus_name]
                    available_seats = final_filtered_df['seats_available'].unique().tolist()
                    bus_price = final_filtered_df['price'].unique().tolist()[0]

                    st.subheader(" Bus Overview")
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric(label=" Available Seats", value=f"{available_seats[0] if available_seats else 'No seats available'}")
                    col_b.metric(label=" Price", value=f"₹{bus_price}")
                    col_c.metric(label=" Rating", value=selected_operator)

                    st.write(f" **Departure Time:** {selected_duration}")
                    st.write(f" **Reaching Time:** {selected_reaching_time}")
                    st.write(f" **Duration:** {selected_duration_time}")
                    st.write(f" **Seat Type:** {selected_seat_type}")
                    st.subheader(" Complete Bus Details")
                    st.dataframe(final_filtered_df)
                    
                    if st.button(" Book Now"):
                        st.session_state.selected_bus = final_filtered_df
                        st.session_state.page = 'booking'

                else:
                    st.subheader(" No buses available with all selected filters.")
                    st.subheader(" Showing the closest matching buses:")

                    selected_criteria = {
                        'bus_type': selected_seat_type,
                        'min_price': selected_price_range[0],
                        'max_price': selected_price_range[1],
                        'departing_time': selected_duration,
                        'reaching_time': selected_reaching_time,
                        'duration': selected_duration_time,
                        'star_rating': selected_operator
                    }

                    closest_matches = find_closest_matches(route_filtered_df, selected_criteria)

                    if not closest_matches.empty:
                        st.header(f" Found {len(closest_matches)} buses with similar criteria:")
                        for i, best_match in closest_matches.iterrows():
                            st.subheader(f" Best Match: {best_match['bus_name']}")
                            col_d, col_e, col_f = st.columns(3)
                            col_d.metric(label=" Available Seats", value=f"{best_match['seats_available']}")
                            col_e.metric(label=" Price", value=f"₹{best_match['price']}")
                            col_f.metric(label=" Rating", value=f"{best_match['star_rating']}")
                            st.write(f" **Departure Time:** {best_match['departing_time']}")
                            st.write(f" **Reaching Time:** {best_match['reaching_time']}")
                            st.write(f" **Duration:** {best_match['duration']}")
                            st.write(f" **Seat Type:** {best_match['bus_type']}")

                            if st.button(f" Book {best_match['bus_name']}", key=f"book_{i}"):
                                st.session_state.selected_bus = best_match
                                st.session_state.page = 'booking'
                                break
                        st.subheader(" Complete Bus Details")
                        st.dataframe(closest_matches, use_container_width=True)
                    else:
                        st.error(" No close matches found.")
        else:
            st.write(" No data available to display.")
    
    # Booking Page
    elif st.session_state.page == 'booking':
        if 'selected_bus' in st.session_state and st.session_state.selected_bus is not None:
            st.header(" Book Your Bus")
            selected_bus = st.session_state.selected_bus.iloc[0] if isinstance(st.session_state.selected_bus, pd.DataFrame) else st.session_state.selected_bus
            st.write(f"**Bus Name:** {selected_bus['bus_name']}")
            st.write(f"**Departure Time:** {selected_bus['departing_time']}")
            st.write(f"**Reaching Time:** {selected_bus['reaching_time']}")
            st.write(f"**Duration:** {selected_bus['duration']}")
            st.write(f"**Seat Type:** {selected_bus['bus_type']}")
            st.write(f"**Price:** ₹{selected_bus['price']}")
            st.write(f"**Available Seats:** {selected_bus['seats_available']}")
            st.write(f"**Rating:** {selected_bus['star_rating']}")

            st.subheader(" Booking Form")
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            phone = st.text_input("Your Phone Number")
            seats = st.select_slider("Select the number of seats", options=list(range(1, 11)), value=1)
            payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Net Banking"])

            if st.button("Confirm Booking"):
                st.subheader(" Booking Confirmed! Thank you for booking with us.")
        else:
            st.write(" No bus selected.")

if __name__ == "__main__":
    main()