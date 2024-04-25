package tg.scam.detector.entity.converter;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import tg.scam.detector.entity.User;

@Converter
public class EnumRoleUserConverter implements AttributeConverter<User.Role, Integer> {
    @Override
    public Integer convertToDatabaseColumn(User.Role role) {
        return role.getId();
    }

    @Override
    public User.Role convertToEntityAttribute(Integer integer) {
        return User.Role.search(integer);
    }
}
