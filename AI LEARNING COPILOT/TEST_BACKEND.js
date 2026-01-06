/**
 * QUICK TEST - Frontend to Backend Connection
 * 
 * Open browser console and run:
 * testBackend()
 */

async function testBackend() {
    console.log('🧪 Testing Backend Connection...\n');
    
    try {
        // Test 1: Health Check
        console.log('1️⃣ Testing Health Check...');
        const healthResponse = await fetch('http://localhost:8000/health');
        console.log('   Response:', healthResponse.status);
        
        if (healthResponse.ok) {
            const health = await healthResponse.json();
            console.log('   ✅ Health Check Passed!', health);
        }
    } catch (error) {
        console.log('   ❌ Health Check Failed:', error.message);
    }
    
    try {
        // Test 2: Generate Content
        console.log('\n2️⃣ Testing Content Generation...');
        const generateResponse = await fetch('http://localhost:8000/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ subject: 'Python' })
        });
        
        console.log('   Response:', generateResponse.status);
        
        if (generateResponse.ok) {
            const data = await generateResponse.json();
            console.log('   ✅ Content Generated!');
            console.log('   Subject:', data.subject);
            console.log('   Topics:', data.total_topics);
            console.log('   Questions:', data.total_questions);
            console.log('\n   📚 First Topic:', data.topics[0].topic);
            console.log('   ❓ First Question:', data.topics[0].questions[0]);
        } else {
            const error = await generateResponse.json();
            console.log('   ❌ Error:', error);
        }
    } catch (error) {
        console.log('   ❌ Test Failed:', error.message);
    }
    
    console.log('\n✅ Test Complete!\n');
}

// Run test immediately when loaded
console.log('📡 Backend Connection Tester Loaded');
console.log('Run: testBackend() in console to test the connection');
