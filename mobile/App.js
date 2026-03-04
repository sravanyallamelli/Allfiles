import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { AuthProvider, useAuth } from './src/context/AuthContext';
import AttendanceScreen from './src/screens/AttendanceScreen';
import HistoryScreen from './src/screens/HistoryScreen';
import LeaveScreen from './src/screens/LeaveScreen';
import LoginScreen from './src/screens/LoginScreen';

const Stack = createNativeStackNavigator();

function Routes() {
  const { token } = useAuth();
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {!token ? (
          <Stack.Screen name="Login" component={LoginScreen} />
        ) : (
          <>
            <Stack.Screen name="Attendance" component={AttendanceScreen} />
            <Stack.Screen name="Leave" component={LeaveScreen} />
            <Stack.Screen name="History" component={HistoryScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes />
    </AuthProvider>
  );
}
