<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use Tests\TestCase;

class UserRegisterTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        // Không cần tạo dữ liệu ở đây vì các test sẽ tự tạo theo trường hợp
    }

    public function test_user_can_register_successfully()
    {
        $response = $this->post(route('register'), [
            'username_regis'   => 'newuser',
            'email'            => 'newuser@example.com',
            'password_regis'   => 'password123',
        ]);

        $response->assertStatus(200);
        $response->assertJson([
            'success' => true,
            'message' => 'Đăng ký thành công! Vui lòng kiểm tra email để kích hoạt tài khoản.'
        ]);

        $this->assertDatabaseHas('tbl_users', [
            'username' => 'newuser',
            'email'    => 'newuser@example.com',
        ]);
    }

    public function test_register_fails_when_username_or_email_exists()
    {
        // Tạo sẵn 1 user
        DB::table('tbl_users')->insert([
            'username'         => 'existinguser',
            'email'            => 'existing@example.com',
            'password'         => md5('somepassword'),
            'isActive'         => 'n',
            'createdDate'      => now(),
            'updatedDate'      => now(),
        ]);

        $response = $this->post(route('register'), [
            'username_regis' => 'existinguser',
            'email'          => 'existing@example.com',
            'password_regis' => 'password123',
        ]);

        $response->assertStatus(200);
        $response->assertJson([
            'success' => false,
            'message' => 'Tên người dùng hoặc email đã tồn tại!',
        ]);
    }
}
