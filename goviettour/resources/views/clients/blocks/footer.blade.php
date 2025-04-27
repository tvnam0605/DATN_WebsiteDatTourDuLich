<!-- footer area start -->
<footer class="main-footer footer-two bgp-bottom bgc-black rel z-15 pt-100 pb-115" style="background-image: url({{ asset('clients/assets/images/backgrounds/footer-two.png')}});">
    <div class="widget-area">
        <div class="container">
            <div class="row row-cols-xxl-5 row-cols-xl-4 row-cols-md-3 row-cols-2">
                <div class="col col-small" data-aos="fade-up" data-aos-duration="1500" data-aos-offset="50">
                    <div class="footer-widget footer-text">
                        <div class="footer-logo mb-40">
                            <a href="{{ route('home') }}"><img src="{{ asset('clients/assets/images/logos/logo.png') }}" alt="Logo"></a>
                        </div>
                        <div class="footer-map">
                            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3903.287790287458!2d108.44162997514084!3d11.95456563635903!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x317112d959f88991%3A0x9c66baf1767356fa!2zVHLGsOG7nW5nIMSQ4bqhaSBI4buNYyDEkMOgIEzhuqF0!5e0!3m2!1svi!2s!4v1743652247560!5m2!1svi!2s" 
                            style="border:0; width: 100%;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                        </div>
                    </div>
                </div>
                <div class="col col-small" data-aos="fade-up" data-aos-delay="50" data-aos-duration="1500" data-aos-offset="50">
                    <div class="footer-widget footer-links ms-sm-5">
                        <div class="footer-title">
                            <h5>Dịch vụ</h5>
                        </div>
                        <ul class="list-style-three">
                            <li><a href="{{ route('team') }}">Hướng dẫn viên du lịch tốt nhất</a></li>
                            <li><a href="{{ route('tours') }}">Đặt tour</a></li>
                            <li><a href="{{ route('tours') }}">Đặt vé</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col col-small" data-aos="fade-up" data-aos-delay="100" data-aos-duration="1500" data-aos-offset="50">
                    <div class="footer-widget footer-links ms-md-4">
                        <div class="footer-title">
                            <h5>Công ty</h5>
                        </div>
                        <ul class="list-style-three">
                            <li><a href="{{ route('about') }}">Giới thiệu về công ty</a></li>
                            <li><a href="{{ route('contact') }}">Việc làm và nghề nghiệp</a></li>
                            <li><a href="{{ route('contact') }}">Liên hệ với chúng tôi</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col col-small" data-aos="fade-up" data-aos-delay="150" data-aos-duration="1500" data-aos-offset="50">
                    <div class="footer-widget footer-links ms-lg-4">
                        <div class="footer-title">
                            <h5>Điểm đến</h5>
                        </div>
                        <ul class="list-style-three">
                            <li><a href="{{ route('destination') }}">Miền Bắc</a></li>
                            <li><a href="{{ route('destination') }}">Miền Trung</a></li>
                            <li><a href="{{ route('destination') }}">Miền Nam</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col col-md-6 col-10 col-small" data-aos="fade-up" data-aos-delay="200" data-aos-duration="1500" data-aos-offset="50">
                    <div class="footer-widget footer-contact">
                        <div class="footer-title">
                            <h5>Liên hệ</h5>
                        </div>
                        <ul class="list-style-one">
                            <li><i class="fal fa-map-marked-alt"></i> 01 Phù Đổng Thiên Vương, Phường 8, Đà Lạt, Lâm Đồng</li>
                            <li><i class="fal fa-envelope"></i> <a
                                    href="mailto:goviettour@gmail.com">goviettour@gmail.com</a></li>
                            <li><i class="fal fa-clock"></i> Thứ 2 - Thứ 6, 08am - 05pm</li>
                            <li><i class="fal fa-phone-volume"></i> <a href="callto:+88012334588">+880 (123)
                                    345 88</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="footer-bottom bg-transparent pt-20 pb-5">
        <div class="container">
            <div class="row">
               <div class="col-lg-5">
                    <div class="copyright-text text-center text-lg-start">
                        <p>@Copy 2024 <a href="\">GoVietTour</a>, All rights reserved</p>
                    </div>
               </div>
               <div class="col-lg-7 text-center text-lg-end">
                   <ul class="footer-bottom-nav">
                    <li><a href="{{ route('about') }}">Điều khoản</a></li>
                    <li><a href="{{ route('about') }}">Chính sách bảo mật</a></li>
                    <li><a href="{{ route('about') }}">Thông báo pháp lý</a></li>
                    <li><a href="{{ route('about') }}">Khả năng truy cập</a></li>
                   </ul>
               </div>
            </div>
        </div>
    </div>
</footer>
<!-- footer area end -->

</div>
<!--End pagewrapper-->

    @if(session('error'))
        <script>
            alert("{{ session('error') }}");
        </script>
    @endif
    <!-- Jquery -->
    <script src="{{asset('clients/assets/js/jquery-3.6.0.min.js')}}"></script>
    <!-- Bootstrap -->
    <script src="{{asset('clients/assets/js/bootstrap.min.js')}}"></script>
    <!-- Appear Js -->
    <script src="{{asset('clients/assets/js/appear.min.js')}}"></script>
    <!-- Slick -->
    <script src="{{asset('clients/assets/js/slick.min.js')}}"></script>
    <!-- Magnific Popup -->
    <script src="{{asset('clients/assets/js/jquery.magnific-popup.min.js')}}"></script>
    <!-- Nice Select -->
    <script src="{{asset('clients/assets/js/jquery.nice-select.min.js')}}"></script>
    <!-- Image Loader -->
    <script src="{{asset('clients/assets/js/imagesloaded.pkgd.min.js')}}"></script>
    <!-- Skillbar -->
    <script src="{{asset('clients/assets/js/skill.bars.jquery.min.js')}}"></script>
    <!-- Jquery UI -->
    <script src="{{asset('clients/assets/js/jquery-ui.min.js')}}"></script>
    <!-- Isotope -->
    <script src="{{asset('clients/assets/js/isotope.pkgd.min.js')}}"></script>
    <!--  AOS Animation -->
    <script src="{{asset('clients/assets/js/aos.js')}}"></script>
    <!-- Custom script -->
    <script src="{{asset('clients/assets/js/script.js')}}"></script>
    {{-- jquery-toast  --}}
    <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>

    {{-- paypal-payment  --}}
    <script src="https://www.paypal.com/sdk/js?client-id=ARN9v4XnRJd84r-8HRkKWQxWBFC3uakGrxkhA-15LpSRvUyqBNRpNEdU93AvbA02x2AglaiCq6zqVPwc"></script>

    <!-- Custom script-->
    <script src="{{asset('clients/assets/js/custom-js.js')}}"></script>
    <script src="{{asset('clients/assets/js/jquery.datetimepicker.full.min.js')}}"></script>

</body>

</html>