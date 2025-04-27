<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class UserLoginTest extends TestCase
{
    use RefreshDatabase, WithFaker;
    /**
     * A basic feature test example.
     *
     * @return void
     */
    protected function setUp(): void
    {
        parent::setUp();
        DB::table('tbl_users')->insert([
            'username' => 'testuser',
            'email' => 'test@example.com',
            'password' => md5('secret123'), // Hash mật khẩu
            'isActive' => 'y',
            'status' => null,
            'createdDate' => now(),
            'updatedDate' => now(),
        ]);
    }
    public function test_user_can_login_with_valid_credentials()
    {$response = $this->post(route('user-login'), [
        'username' => 'testuser',
        'password' => 'secret123'
    ]);
    
    $response->assertStatus(200);
    $response->assertJson([
        'success' => true,
        'message' => 'Đăng nhập thành công!',
    ]);
    
    }
    public function test_user_cannot_login_with_wrong_password()
    {
        $response = $this->post(route('user-login'), [
            'username' => 'testuser',
            'password' => 'sai_mk'
        ]);
        
        $response->assertStatus(200); // vì vẫn trả về JSON 200
        $response->assertJson([
            'success' => false,
        ]);
    }
    public function test_user_cannot_login_if_inactive()
    {
        DB::table('tbl_users')->where('username', 'testuser')->update([
            'isActive' => 'n'
        ]);
        
        $response = $this->post(route('user-login'), [
            'username' => 'testuser',
            'password' => 'secret123'
        ]);
        
        $response->assertStatus(200);
        $response->assertJson([
            'success' => false,
        ]);
    }
}