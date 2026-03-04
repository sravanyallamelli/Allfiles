import { Button, View } from 'react-native';
import { api } from '../api/client';

export default function AttendanceScreen({ navigation }) {
  return (
    <View style={{ padding: 16, gap: 10 }}>
      <Button title="Check In" onPress={() => api.post('/attendance/check-in')} />
      <Button title="Check Out" onPress={() => api.post('/attendance/check-out')} />
      <Button title="Apply Leave" onPress={() => navigation.navigate('Leave')} />
      <Button title="History" onPress={() => navigation.navigate('History')} />
    </View>
  );
}
