<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('tbl_users', function (Blueprint $table) {
            $table->id('userId');  // Sử dụng trường 'userId' làm primary key mặc định
            $table->string('google_id', 50)->nullable();
            $table->string('fullName', 255)->nullable();
            $table->string('username', 50);
            $table->string('password', 255);
            $table->string('email', 255);
            $table->string('avatar', 255)->nullable();
            $table->string('phoneNumber', 15)->nullable();
            $table->string('address', 255)->nullable();
            $table->string('ipAdress', 50)->nullable();
            $table->enum('isActive', ['y', 'n'])->default('n');
            $table->enum('status', ['d', 'b'])->nullable();
            $table->timestamp('createdDate')->useCurrent();
            $table->timestamp('updatedDate')->useCurrent()->useCurrentOnUpdate();
            $table->string('activation_token', 255)->nullable();
            
            // Xóa dòng này vì Laravel đã tự động tạo khóa chính với `$table->id()`
            // $table->primary('userId');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('tbl_users');
    }
};
